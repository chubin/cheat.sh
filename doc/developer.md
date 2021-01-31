## Developer Keys

If you have a developer key, you can provide it in your queries
to get access to experimental cheat.sh features.
The developer key must be specified as the `X-Cheatsh-Key` header of the query.

To check, if you key is valid, query `/:authorized`:

```
$ curl -H "X-Cheatsh-Key: 2ecf6cba-a8b2-04a7-7a51-XXXX" http://127.0.0.1:8002/:authorized
AUTHORIZED (developer)

$ curl -H "X-Cheatsh-Key: 2ecf6cba-a8b2-04a7-7a51-YYYY" http://127.0.0.1:8002/:authorized
NOT AUTHORIZED
```

If you use editor plugins to access *cheat.sh*, see the plugin documentation
for information about key usage.
