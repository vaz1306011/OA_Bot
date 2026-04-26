# OA_Bot

**_Discord Bot_**

🇯🇵 日本語のドキュメントはこちら → [README_JP.md](README_JP.md)  
🇨🇳 中文說明文件 → [README.md](README.md)

This is a multi-purpose Discord bot developed mainly in a Chinese environment.

---

## 目次

- [概要](#概要)
- [インストールと起動方法](#インストールと起動方法)
- [主な機能](#主な機能)

---

## [ボットをサーバーに招待する](https://discord.com/api/oauth2/authorize?client_id=799467265010565120&permissions=2147575872&scope=bot)

---

## 概要

本プロジェクトは、Discord でよく利用される機能を一つにまとめた Bot です。  
ランダム選択、メッセージ管理、投票、エンタメ機能、音楽再生などを提供します。

複数の操作をコマンド化することで、サーバー運用の効率化を目的としています。

---

## インストールと起動方法

### 1. リポジトリをクローン

```bash
git clone https://github.com/vaz1306011/OA_Bot
cd OA_Bot
```

### 2. Bot Token の設定

`.env.example` を `.env` にコピーまたはリネームします。

```bash
cp .env.example .env
```

その後、`.env` 内の Token を自分の Discord Bot Token に変更します。

### 3. 管理者 ID の設定

`data/data.json.example` を `data/data.json` にコピーまたはリネームします。

```bash
cp data/data.json.example data/data.json
```

その後、`data/data.json` の `owner_ids` に自分の Discord ユーザー ID を設定します。

### 4. Bot の起動

通常起動：

```bash
docker compose up --build
```

バックグラウンド起動：

```bash
docker compose up --build -d
```

---

## 主な機能

### 音楽再生

<img width="700" src=".readme/music-play.gif"/>

---

### ランダム選択

<img width="700" src=".readme/random-choose.gif"/>

---

### 指定メッセージの一括削除

<img width="700" src=".readme/clean-message.gif"/>

---

### キーワード検知機能のオン / オフ

    /omi guild <status>
    /omi channel <status>
    /omi user <status>

---

### メンバー、ロール、チャンネル、サーバー ID の取得

    /id guild
    /id role <role>
    /id channel <channel>
    /id member [member]

---

### Bot の ping を確認

    /ping

---

### ロールの追加 / 削除

    /role add <member> <role>
    /role remove <member> <role>

---

### サイコロ

    /roll [min] [max]

---

### 匿名発言

    /say <message>

---

### 投票

    /vote <content>

---

### じゃんけん

    /vow [epc] [m1] [m2] [m3] [m4] [m5] [m6] [m7] [m8] [m9] [m10]

---

To be continued...
