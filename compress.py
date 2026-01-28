from pathlib import Path

from PIL import Image
from loguru import logger


def compress_images_recursively(
        source_dir: Path,
        target_dir: Path,
        quality: int = 85,
) -> None:
    """
    递归读取 source_dir 下所有 .jpg 文件，按指定质量压缩后保存到 target_dir，
    保持原始目录结构。

    :param source_dir: 源目录路径，包含原始 jpg 文件
    :param target_dir: 目标目录路径，压缩后的文件保存位置
    :param quality: JPEG 压缩质量，范围 1-95，越高质量越好，默认 85
    """
    # 确保目标目录存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 查找所有 .jpg 和 .JPG 文件（区分大小写）
    jpg_files = source_dir.rglob("*.jpg")

    for src_path in jpg_files:
        # 计算相对于源目录的相对路径
        rel_path = src_path.relative_to(source_dir)
        dst_path = target_dir / rel_path

        # 确保目标文件的父目录存在
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # 打开并压缩图像
        with Image.open(src_path) as img:
            # 确保图像是 RGB 模式（避免 RGBA 或 P 模式保存出错）
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # 保存为指定质量的 JPEG
            img.save(dst_path, "JPEG", quality=quality, optimize=True)

        logger.info(f"已压缩: {src_path} --> {dst_path}")

    logger.info(f"压缩完成：共处理 {len(list(jpg_files))} 个文件")


if __name__ == "__main__":
    # 配置路径（请根据实际路径调整）
    SOURCE_DIR = Path("MyGICA-fast")
    TARGET_DIR = Path("MyGICA-fast-small-50")
    QUALITY = 50  # 可调整：75~95 为常用范围，85 平衡清晰度与体积

    compress_images_recursively(SOURCE_DIR, TARGET_DIR, QUALITY)
