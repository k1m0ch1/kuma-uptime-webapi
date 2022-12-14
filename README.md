# Kuma Uptime WebAPI

The Stateless Web API for [uptime-kuma](https://github.com/louislam/uptime-kuma) with cool wrapper from https://github.com/lucasheld/uptime-kuma-api

yes I know my code is kinda trash, but I desperately needs the web API for uptime kuma to add the monitoring via API, anyway I love using uptime kuma since 2021, the status page, the monitor and anything else

eFishery using this since 2021, and we love it.

## How to use

you could use the image from `ghcr.io/k1m0ch1/kuma-uptime-webapi:master`

you only need to use environment variable with key `KUMA_URL` and value with the kuma uptime URL

and for every request you need to add the `Authorization` Header with basic auth
ex:
```
Authorization: Basic YWRtaW46d2hhdGFyZXlvdWxvb2tpbmdkaW13aXQ=
```

## Available endpoint

`/status`
`/monitors`
`/monitor/add`

## Next Todo

- making a proper doc
