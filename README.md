# on-behalf-of-flow-function


## ローカル実行
`local.setings.json` の `Values` に以下を登録

```
"CLIENT_ID" : <クライアント ID>,
"CLIENT_SECRET" : <クライアントシークレット>,
"TENANT_ID" : <テナント ID>
```

## Azure 実行
- Azure ポータルの「構成」より環境変数のセットアップが必要
- `CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID` の登録が必要