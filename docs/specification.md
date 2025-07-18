# 美術館探索アプリケーション Gallery-Hunt 仕様書
## 概要
受動的になりがちな芸術鑑賞ををより充実させるためのアプリケーションです。
本アプリケーションは、来館者が自らクイズを解きながら作品を探し、LLMとのインタラクションを通じて芸術と深く関わる体験を提供します。
これにより、美術館の魅力を再発見し、より多くの人々が作品に親しみを感じるきっかけを創出します。 

## 主な機能要件
**作品探しクイズ機能**
- **ターゲット作品の選定:** アプリケーションは、美術館の作品データベースからランダムに1つの作品をターゲットとして選定します。

- **ヒントの提示:**
LLMが選定されたターゲット作品に関するヒントを生成し、ユーザーに提示します。
ユーザーの進行状況や要求に応じて、ヒントの難易度を調整・提供できるようにします。

- **ユーザーからの回答/質問:** 
ユーザーはヒントを元に美術館内を探索し、作品を発見できない場合はLLMに追加のヒントを要求したり、見つけたと思われる作品名を伝えて確認したりできます。

- **LLMによる評価とフィードバック:**
ユーザーの回答（見つけた作品名など）がターゲット作品と一致するかをLLMが評価し、正誤を通知します。
正解の場合、LLMはその作品に関する詳細な情報や豆知識を提供し、鑑賞を深めます。
ユーザーが間違った方向に進んでいる場合、LLMがさりげなくヒントを修正したり、別の視点を示したりして誘導します。

- **ゲームの終了と継続:** 
ユーザーはゲームを終了するか、次の作品探しに挑戦するかを選択できます。

**鑑賞支援機能（将来的な拡張）**
- **パーソナライズされた解説:** 
来館者の興味や知識レベルに応じて、作品の背景、作者の意図、関連する歴史的・文化的文脈などを深掘りした解説を提供します。
- **インタラクティブQ&A:** ユーザーが作品に関する疑問をLLMに自由に投げかけ、即座に回答を得られる機能を提供します。

## 使用技術
- React + Typescript
- Vite
- Python
- llama-cpp-python
