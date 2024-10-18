from moviepy.editor import VideoFileClip
from PIL import Image
import colorsys

def process_frame(frame, remove_colors_rgb=[]):
    """フレームを処理する関数

    Args:
        frame: NumPy配列のフレーム
        remove_colors_rgb (list of tuple, optional): RGBで指定する除去する色のリスト. Defaults to [].

    Returns:
        PIL.Image.Image: 処理後のフレーム
    """
    img = Image.fromarray(frame)

    # 緑系統の色を透過
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        r, g, b, a = item
        h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)

        if (60 <= h * 360 <= 180 and s > 0.1) or (item[:3] in remove_colors_rgb):  # HSV色空間の緑色または指定したRGB色の場合
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)

    # 上部15%、下部8%を削除
    width, height = img.size
    top = int(height * 0.15)
    bottom = int(height * 0.92)
    img = img.crop((0, top, width, bottom))

    # 中央を基準に正方形にリサイズ
    new_size = min(img.width, img.height)
    left = (img.width - new_size) // 2
    top = (img.height - new_size) // 2
    right = left + new_size
    bottom = top + new_size
    img = img.crop((left, top, right, bottom))

    img = img.resize((int(img.width * 36 / img.height), 36))

    return img

def process_video(video_path, output_dir, remove_colors_rgb=[]):
    """動画を処理する関数

    Args:
        video_path (str): 動画ファイルのパス
        output_dir (str): 出力ディレクトリのパス
        remove_colors_rgb (list of tuple, optional): RGBで指定する除去する色のリスト. Defaults to [].
    """
    video = VideoFileClip(video_path)
    for i, frame in enumerate(video.iter_frames()):
        img = process_frame(frame, remove_colors_rgb)
        img.save(f"{output_dir}/frame_{i:04d}.png")

# --- 実行 ---
video_path = "movie.mp4"  # 動画ファイルのパス
output_dir = "output"  # 出力ディレクトリのパス

# RGBで指定する除去する色のリスト
remove_colors_rgb = [
    (0, 255, 0),
    (1, 254, 0),
    (6,252,39),
    (6,255,40),
    (9,183,31),
    (0,0,0),
    (15,230,40),
    (6,252,39),
    (1,0,0),
    (9,184,31),
    (10,183,32),
    (1,255,37),
    (5,254,39),
    (10,182,32),
    (2,0,0),
    (61,117,68),
    (23,246,55),
    (25,242,48),
    (128,202,126),
    (3,253,36),
    (22,251,52),
    (22,246,53),
    (6,255,41),
    (10,184,31),
    (0,252,33),
    (109,237,126),
    (3,254,37),
    (5,253,39),
    (41,245,70),
    (8,253,40),
    (15,252,48),
    (6,253,39),
    (4,255,38),
    (0,255,37),
    (39,247,68),
    (1,252,36),
    (0,253,33),
    (114,231,130),
    (0,253,32),
    (140,221,150),
    (146,214,154),
    (10,251,43),
    (11,215,40),
    (5,253,38),
    (171,235,167),
    (6,251,38),
    (0,253,34),
    (55,238,81),
    (43,241,73),
    (80,242,101),
    (24,219,41),
    (60,249,89),
    (78,212,75),
    (34,234,53),
    (2,255,38),
    (8,252,40),
    (70,214,68),
    (62,243,79),
    (5,255,38),
    (29,248,52),
    (5,253,39),
    (11,238,41),
    (2,255,37),
    (10,247,41),
    (0,255,36),
    (37,230,52),
    (25,238,48),
    (78,243,102),
    (89,245,113),
    (55,246,82),
    (141,243,157),
    (34,240,61),
    (43,241,71),
    (0,250,34),
    (0,255,35),
    # ここに他の除去したい色を追加
]

process_video(video_path, output_dir, remove_colors_rgb)