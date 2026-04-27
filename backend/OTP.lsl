// ============================================================
//  VASTIK OTP Delivery — LSL Script
//  Push-based architecture:
//    1. On startup/region restart: request a URL via llRequestURL()
//    2. POST the URL to the Django backend for registration
//    3. Listen for incoming OTP delivery requests from the backend
//    4. Deliver OTPs to avatars via llInstantMessage()
// ============================================================

// ── CONFIG ────────────────────────────────────────────────────
// Your Django backend base URL (no trailing slash)
string BACKEND_URL    = "https://your-vastik-server.com";
// The endpoint where we register our object URL
string REGISTER_PATH  = "/api/v1/sl-bridge/register-url/";
// Shared secret — MUST match SL_BRIDGE_SECRET in your Django .env
string SHARED_SECRET  = "change-me-to-a-random-secret";

// ── STATE ─────────────────────────────────────────────────────
string  gObjectURL    = "";      // Our current dynamic URL
key     gURLRequest   = NULL_KEY; // llRequestURL request ID
key     gHTTPRegister = NULL_KEY; // Registration HTTP request ID
integer gRetryCount   = 0;       // Retry counter for registration
integer gMaxRetries   = 5;       // Max registration retries

// ── HELPERS ───────────────────────────────────────────────────

// URL-decode a string (handles %20, +, etc.)
// LSL doesn't have a built-in URL decoder, so we handle common cases
string urlDecode(string src)
{
    return llUnescapeURL(src);
}

// Extract a value from a simple "key=value&key2=value2" body
string getFormValue(string body, string fieldName)
{
    // Split by &
    list pairs = llParseString2List(body, ["&"], []);
    integer i;
    integer count = llGetListLength(pairs);
    for (i = 0; i < count; i++)
    {
        string pair = llList2String(pairs, i);
        list kv = llParseString2List(pair, ["="], []);
        if (llGetListLength(kv) >= 2)
        {
            string key = llList2String(kv, 0);
            if (key == fieldName)
            {
                // Rejoin in case value contained '='
                string val = llList2String(kv, 1);
                integer j;
                for (j = 2; j < llGetListLength(kv); j++)
                {
                    val += "=" + llList2String(kv, j);
                }
                return urlDecode(val);
            }
        }
    }
    return "";
}

// Request a new URL from Second Life
requestNewURL()
{
    llSetText("VASTIK OTP Bot\nRequesting URL...", <1, 0.8, 0.2>, 1.0);
    gObjectURL = "";
    gURLRequest = llRequestURL();
}

// Register our URL with the Django backend
registerWithBackend()
{
    if (gObjectURL == "")
    {
        llOwnerSay("[VASTIK] No object URL to register.");
        return;
    }

    string body = "object_url=" + llEscapeURL(gObjectURL)
                + "&secret=" + llEscapeURL(SHARED_SECRET);

    llOwnerSay("[VASTIK] Registering URL with backend...");

    gHTTPRegister = llHTTPRequest(
        BACKEND_URL + REGISTER_PATH,
        [
            HTTP_METHOD,      "POST",
            HTTP_MIMETYPE,    "application/x-www-form-urlencoded",
            HTTP_BODY_MAXLENGTH, 4096
        ],
        body
    );
}

// Retry registration with exponential backoff
retryRegistration()
{
    gRetryCount++;
    if (gRetryCount > gMaxRetries)
    {
        llOwnerSay("[VASTIK] Max registration retries reached. "
                 + "Will try again on next region restart or script reset.");
        llSetText("VASTIK OTP Bot\n⚠ Registration failed", <1, 0.3, 0.3>, 1.0);
        return;
    }

    // Exponential backoff: 5s, 10s, 20s, 40s, 80s
    float delay = 5.0 * llPow(2.0, (float)(gRetryCount - 1));
    llOwnerSay("[VASTIK] Retrying registration in " + (string)((integer)delay)
             + " seconds (attempt " + (string)gRetryCount + "/" + (string)gMaxRetries + ")");
    llSetTimerEvent(delay);
}


// ── MAIN ──────────────────────────────────────────────────────
default
{
    state_entry()
    {
        llOwnerSay("[VASTIK] OTP delivery script starting...");
        gRetryCount = 0;
        requestNewURL();
    }

    on_rez(integer start_param)
    {
        // Re-initialize when the object is rezzed
        llResetScript();
    }

    changed(integer change)
    {
        // Re-request URL on region restart or region change
        if (change & (CHANGED_REGION_START | CHANGED_REGION))
        {
            llOwnerSay("[VASTIK] Region change detected — re-requesting URL...");
            gRetryCount = 0;
            requestNewURL();
        }
    }

    // ── Receive the URL from llRequestURL() ──────────────────
    url_request(key request_id, string method, string body)
    {
        // This is called when llRequestURL() completes
        if (request_id == gURLRequest)
        {
            if (method == URL_REQUEST_GRANTED)
            {
                gObjectURL = body;
                llOwnerSay("[VASTIK] Object URL received: " + gObjectURL);
                llSetText("VASTIK OTP Bot\nRegistering...", <1, 0.8, 0.2>, 1.0);
                gRetryCount = 0;
                registerWithBackend();
            }
            else // URL_REQUEST_DENIED
            {
                llOwnerSay("[VASTIK] URL request denied: " + body);
                llSetText("VASTIK OTP Bot\n⚠ URL denied", <1, 0.3, 0.3>, 1.0);
                // Retry after a delay
                llSetTimerEvent(30.0);
            }
            return;
        }

        // ── Incoming request from the Django backend ─────────
        // method will be "POST", "GET", etc.
        if (method == "POST")
        {
            // Parse the form-encoded body:
            //   secret=xxx&avatar_name=xxx&otp_code=123456
            string inSecret   = getFormValue(body, "secret");
            string avatarName = getFormValue(body, "avatar_name");
            string otpCode    = getFormValue(body, "otp_code");

            // Validate shared secret
            if (inSecret != SHARED_SECRET)
            {
                llHTTPResponse(request_id, 403, "Forbidden");
                llOwnerSay("[VASTIK] Rejected OTP request — invalid secret");
                return;
            }

            // Validate required fields
            if (avatarName == "" || otpCode == "")
            {
                llHTTPResponse(request_id, 400, "Missing avatar_name or otp_code");
                llOwnerSay("[VASTIK] Rejected OTP request — missing fields");
                return;
            }

            // Look up the avatar key from their username
            // llName2Key expects the username (e.g. "firstname.lastname" or "username")
            key avatarKey = llName2Key(avatarName);

            if (avatarKey == NULL_KEY)
            {
                // If llName2Key fails, try with ".resident" suffix
                // (for single-name accounts)
                if (llSubStringIndex(avatarName, ".") == -1)
                {
                    avatarKey = llName2Key(avatarName + ".resident");
                }
            }

            if (avatarKey == NULL_KEY)
            {
                llHTTPResponse(request_id, 404, "Avatar not found: " + avatarName);
                llOwnerSay("[VASTIK] Could not find avatar key for: " + avatarName);
                return;
            }

            // Send the OTP via instant message
            string message = "[VASTIK] 🔐 Your OTP verification code is: " + otpCode
                           + "\n\nPlease enter this code on the VASTIK website to verify your identity."
                           + "\nThis code expires in 10 minutes."
                           + "\n\nIf you did not request this, please ignore this message.";

            llInstantMessage(avatarKey, message);

            llHTTPResponse(request_id, 200, "OTP delivered to " + avatarName);
            llOwnerSay("[VASTIK] ✓ OTP delivered to " + avatarName + " (" + (string)avatarKey + ")");
        }
        else if (method == "GET")
        {
            // Health check — backend can ping this to verify the URL is alive
            llHTTPResponse(request_id, 200, "VASTIK OTP Bot active");
        }
        else
        {
            llHTTPResponse(request_id, 405, "Method not allowed");
        }
    }

    // ── Handle outbound HTTP responses (registration) ────────
    http_response(key request_id, integer status_code, list metadata, string body)
    {
        if (request_id != gHTTPRegister) return;
        gHTTPRegister = NULL_KEY;

        if (status_code == 200)
        {
            llOwnerSay("[VASTIK] ✓ Successfully registered with backend!");
            llSetText("VASTIK OTP Bot\n✓ Online & Ready", <0.2, 1, 0.4>, 1.0);
            gRetryCount = 0;
            // Stop any pending retry timer
            llSetTimerEvent(0.0);
        }
        else
        {
            llOwnerSay("[VASTIK] Registration failed (HTTP " + (string)status_code + "): " + body);
            retryRegistration();
        }
    }

    // ── Timer for retries ────────────────────────────────────
    timer()
    {
        llSetTimerEvent(0.0); // Stop the timer

        if (gObjectURL == "")
        {
            // URL was denied — try requesting again
            requestNewURL();
        }
        else
        {
            // Registration failed — retry
            registerWithBackend();
        }
    }

    // ── Owner touch for manual status / re-registration ──────
    touch_start(integer total)
    {
        if (llDetectedKey(0) == llGetOwner())
        {
            if (gObjectURL == "")
            {
                llOwnerSay("[VASTIK] No URL assigned. Requesting new URL...");
                requestNewURL();
            }
            else
            {
                llOwnerSay("[VASTIK] Status:"
                         + "\n  URL: " + gObjectURL
                         + "\n  Registered: " + (gHTTPRegister == NULL_KEY ? "Yes" : "Pending...")
                         + "\n\nTouching again will re-register.");
                registerWithBackend();
            }
        }
        else
        {
            llInstantMessage(llDetectedKey(0),
                "[VASTIK] This is the VASTIK OTP verification bot. "
              + "Please use the website to request an OTP.");
        }
    }
}