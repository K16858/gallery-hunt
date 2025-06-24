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


def get_artwork_info(json_file_path):
    """
    指定されたJSONファイルからランダムな作品の情報を取得し、フォーマットされた文字列として返す
    """
    artwork = get_random_artwork(json_file_path)
    artwork_info = ""
    if artwork:
        for key, value in artwork.items():
            artwork_info += f"{key}: {value}\n"
    else:
        artwork_info = "作品情報の取得に失敗しました。"
    return artwork_info.strip()
