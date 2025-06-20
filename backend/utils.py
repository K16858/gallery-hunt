import json
import random

def get_random_artwork(json_file_path):
    """
    JSONファイルから作品データを読み込み、ランダムに1つの作品を返す
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            artworks = json.load(f)
    except FileNotFoundError:
        print(f"エラー: ファイル '{json_file_path}' が見つからない")
        return None
    except json.JSONDecodeError:
        print(f"エラー: '{json_file_path}' のJSON形式が不正")
        return None
    
    if not artworks:
        print("エラー: 作品データが空")
        return None

    return random.choice(artworks)
