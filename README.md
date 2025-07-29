# GraphQL expert in Multi-agent system (WIP)

This project aims to build a demo for GraphQL expert agent which can be invoked in a multi-agent system (building with langGraph).

## Structure Design

```
User Input
    ↓
Orchestrator (Routing Decision)
    ↓
    ├── Graphql Agent (Graphql Queries) 
    ├── Weather Agent (Weather Queries) 
    └── format_response (Response Formatting)
    ↓
Return to User
```

## Usage

You should run mcp server before you test the GraphQL agent or run the chatbot

### Run mcp server

```bash
  uv run src/tools/server.py
```

### Run chatbot

```bash
  uv run src/main.py
```

### Test GraphQL agent

```bash
  uv run simple_test.py
```

## Example

The following is a demonstration for chatbot:

```
Mutil-agent Chatbot
==================================================
Supported Features:
- Query Weather
- GraphQL Data Queries
- Input 'quit' or 'exit' to quit
==================================================

User: 上海今天什么天气

Agent is thinking...
Agent: 你好！我是你的天气专家Weather Agent。根据模拟数据，今天上海的天气情况如下：

  - **天气**：多云
  - **气温**：最高约25°C，最低约18°C
  - **湿度**：75%
  - **风速**：东南风，约15公里/小时

建议大家出门时可以穿轻便的衣物，并携带一把雨伞，以备不时之需！如果你还有其他天气查询，随时告诉我哦！

User: 北京今天天气怎么样？

Agent is thinking...
Agent: 你好！我是Weather Agent。今天北京的天气晴朗，气温大约在20°C到28°C之间，湿度适中，风速为10公里每小时。适合户外活动哦！如果你需要出门，记得保持适当的防晒哦！如果还有其他天气相关的问题，随时问我！

User: 帮我查一下sujiyan.eth的身份信息

Agent is thinking...
Agent: sujiyan.eth的身份信息如下：

- 身份标识(identity)： sujiyan.eth
- 平台(platform)： ENS
- 网络(network)： Ethereum
- 以太坊地址(address)： 0x7cbba07e31dc7b12bb69a1209c5b11a8ac50acf5
- 显示名称(displayName)： sujiyan.eth
- 头像(avatar)： ![头像](https://i.imgur.com/rkMlngS_d.webp?maxwidth=640&shape=thumb&fidelity=medium)
- 相关文本(texts)包括：
  - 个人网址: https://mask.io
  - 邮箱: suji.yan@dimension.im
  - 头部图片: https://rainbow.mypinata.cloud/ipfs/QmUpk4q82RFMTLU9nLtheenjMn56UMJsAMrHs55PK1iJtW
  - Snapshot链接: ipns://storage.snapshot.page/registry/0x934B510D4C9103E6a87AEf13b816fb080286D649/sujiyan.eth
  - GitHub账号: tedko
  - Twitter账号: suji_yan
  - Instagram账号: suji_yan_
  - ENS DAO代表相关链接: https://discuss.ens.domains/t/ens-dao-delegate-applications/815/526?u=sujiyan
- 关联的以太坊地址信息：
  - 地址: 0x7cbba07e31dc7b12bb69a1209c5b11a8ac50acf5 (Ethereum网络)

如果需要查询全部身份图谱信息，或者其他内容，请告诉我。

User: 帮我查帮我查一下 sujiyan.eth的各平台的身份吧

Agent is thinking...
Agent: sujiyan.eth 的各平台身份信息如下：

- ens 平台（Ethereum 网络）身份有：
  - sujiyan.eth
  - citizenfour.eth
  - terrybranstad.eth
  - niconico.eth
  - 🇺🇸❤🇨🇳.eth
  - suji.eth
  - kmt.eth
  - pawoo.eth
  - nostr.box.eth
  - 🇨🇳❤🇺🇸.eth
  - mstdn.eth

- basenames 平台（Ethereum 网络）身份：
  - suji.base.eth

- lens 平台（Ethereum 网络）身份：
  - sujidaily.lens
  - sujiyan.lens

- ethereum 平台（Ethereum 网络）身份（多个以 0x 开头的地址）：
  - 0x7cbba07e31dc7b12bb69a1209c5b11a8ac50acf5
  - 0xde0c0ac846a80e52a7825ed4b304ef3283a36b1a
  - 0x609ea456945954e9e06d903f080ad6cdd9e39b57
  - 等等多个地址

- nextid 平台：
  - 0x028f936e528de34fc95179780751ec21256825ce604950580978a8961c5af03e50

- solana 平台（Solana 网络）身份：
  - 24ywRTze3X2fUez6mkC9WCaKPVdMF6ykgzLq7wavjvap
  - B9HNZSGtXME8wkrJmf4VYX1p7LuuFgVai6TFQ2pZ74c6
  - 9mUxj781h7UXDFcbesr1YUfVGD2kQZgsUMc5kzpL9g65
  - GnwbTBS1d9cGHCoeBhamZsXsKtTe5gGYj7JK31QpkxQx

- firefly 平台：
  - 1918273493

- bitcoin 平台（Bitcoin 网络）身份：
  - 3NdNQWaoLr3fXfzPtHoQfhy3nuEpB8Dhh1

- bluesky 平台：
  - suji.bsky.social

- keybase 平台：
  - sujiyan

- reddit 平台：
  - jktedko

- discord 平台：
  - sujiyan

- farcaster 平台（Ethereum 网络）身份：
  - dragon2024
  - suji

- github 平台：
  - tedko

- twitter 平台：
  - suji_yan

这是 sujiyan.eth 在多个区块链和社交平台上的身份列表。您需要了解某个身份的详细信息吗？

 User: quit
bye
```