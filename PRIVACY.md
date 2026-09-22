# Privacy Policy

This plugin connects a Dify application to a **self-hosted Darkmoon Dashboard API**
that you operate. Darkmoon is self-hosted; there is no public hosted endpoint and
no service run by the plugin author.

## What the plugin sends

- **To your Darkmoon instance only:** the base URL, dashboard username and password
  you configure (used to obtain a short-lived JWT from `POST /api/v1/auth/login`),
  and the parameters of the action you invoke (for example the target of a pentest
  or a campaign id). These go only to the base URL you configured.
- The plugin does **not** send any data to the plugin author or to any third party.

## What the plugin stores or logs

- The plugin stores nothing of its own. Credentials are held by Dify's own
  credential store, as with any Dify tool provider.
- Error messages surface only the Darkmoon API's own error detail. The plugin is
  written so that the password, the JWT and any credential reference are never
  placed into an error message or log line.

## Remediation credentials

The optional remediation feature (a paid Darkmoon Pro capability) uses an **opaque
credential reference** - an id of a credential stored inside Darkmoon's own
encrypted vault. Raw source-control tokens never travel through this plugin.

## Data controller

You, the operator of the Darkmoon instance, are the data controller for any data
processed by your Darkmoon deployment. Refer to your own Darkmoon deployment's
configuration and to the Darkmoon documentation for how Darkmoon itself handles
assessment data.

## Contact

Questions about this plugin: open an issue at
https://github.com/ASCIT31/dify-plugin-darkmoon
