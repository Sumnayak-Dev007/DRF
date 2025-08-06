<h2>🔐 JSON Web Authentication</h2>

<h3>⚠️ What Happens When the Access Token Expires?</h3>
<p>
Yes — the <strong>access token</strong> will expire soon, even if the <strong>refresh token</strong> is still valid.
</p>
<p>
But here’s the key point:
</p>
<blockquote>
You don’t need to log in again when the access token expires —<br>
You just use the <strong>refresh token</strong> to get a new access token.
</blockquote>

<h3>🧠 Why Make Access Tokens Short?</h3>
<p>This is a <strong>security feature</strong>:</p>
<ul>
  <li>If an attacker gets an access token, it’s only valid for a few minutes.</li>
  <li>Even if the user stays logged in all day, the server stays secure by rotating access tokens.</li>
</ul>

<h3>🔄 What Keeps the Session Alive?</h3>
<p>
🔑 The <strong>refresh token</strong> is what keeps your session alive for hours or days.
</p>
<p>
So even though access tokens expire quickly, the refresh token allows the user to stay logged in without re-entering their credentials.
</p>
<p><strong>This is called token rotation.</strong></p>

<h3>🔒 What Happens When the Refresh Token Expires?</h3>
<ul>
  <li>You <strong>cannot</strong> get new access tokens anymore.</li>
  <li>The user <strong>must log in again</strong> (username + password).</li>
</ul>

<h3>Algolia Instant Search</h3>
<p>https://www.algolia.com/doc/guides/building-search-ui/installation/js/#directly-in-your-page</p>



