import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(".").resolve()

# (원하면 여기에 폴더 더 추가 가능)
TARGET_IMAGE_DIR_NAMES = {"이미지"}  # 이런 폴더를 "images"로 바꾼다.
NEW_IMAGE_DIR_NAME = "images"

# image (n).png  -> image_n.png
IMG_PAREN_RE = re.compile(r"^image\s*\((\d+)\)\.(png|jpg|jpeg|gif|webp)$", re.IGNORECASE)

# md에서 ./이미지/xxx 또는 ./images/xxx 모두 찾아서 바꿀 때 사용
MD_IMAGE_LINK_RE = re.compile(r'(!\[[^\]]*\]\()([^)]+)(\))')

def run_git_mv(src: Path, dst: Path):
    # git mv는 경로 구분자 문제 줄이려고 POSIX 형태로 넘김
    src_s = src.as_posix()
    dst_s = dst.as_posix()
    subprocess.check_call(["git", "mv", "--", src_s, dst_s])

def safe_read_text(p: Path) -> str:
    # md는 보통 utf-8, 혹시 깨진 경우를 대비해 errors="replace"
    return p.read_text(encoding="utf-8", errors="replace")

def safe_write_text(p: Path, s: str):
    p.write_text(s, encoding="utf-8", newline="\n")

def url_decode_basic(s: str) -> str:
    # 최소한의 디코드: %20만 공백으로
    return s.replace("%20", " ")

def url_encode_spaces(s: str) -> str:
    return s.replace(" ", "%20")

def main():
    # 1) 이미지 폴더(이름이 "이미지") -> "images" 로 git mv
    img_dirs = []
    for p in REPO_ROOT.rglob("*"):
        if p.is_dir() and p.name in TARGET_IMAGE_DIR_NAMES:
            img_dirs.append(p)

    # 깊은 경로부터 먼저 바꾸기 (하위부터)
    img_dirs.sort(key=lambda x: len(str(x)), reverse=True)

    dir_rename_map = {}
    for old_dir in img_dirs:
        new_dir = old_dir.with_name(NEW_IMAGE_DIR_NAME)
        if new_dir.exists():
            # 이미 images가 있으면 스킵 (충돌 방지)
            continue
        print(f"[DIR] {old_dir} -> {new_dir}")
        run_git_mv(old_dir, new_dir)
        dir_rename_map[old_dir.as_posix()] = new_dir.as_posix()

    # 2) images 폴더 내부 파일명 정리 (image (n).png -> image_n.png)
    file_rename_map = {}
    for images_dir in REPO_ROOT.rglob(NEW_IMAGE_DIR_NAME):
        if not images_dir.is_dir():
            continue

        for f in images_dir.iterdir():
            if not f.is_file():
                continue

            m = IMG_PAREN_RE.match(f.name)
            if m:
                n = m.group(1)
                ext = m.group(2).lower()
                new_name = f"image_{n}.{ext}"
                new_path = f.with_name(new_name)
                if new_path.exists():
                    continue
                print(f"[FILE] {f} -> {new_path}")
                run_git_mv(f, new_path)
                file_rename_map[f.as_posix()] = new_path.as_posix()

    # 3) 모든 md 파일에서 링크 경로 치환
    md_files = list(REPO_ROOT.rglob("*.md"))
    for md in md_files:
        old = safe_read_text(md)
        updated = old

        def replace_link(match: re.Match) -> str:
            prefix, link, suffix = match.group(1), match.group(2), match.group(3)

            # 링크에 공백/괄호가 %20 등으로 인코딩돼 있을 수 있어 최소 디코드해서 비교
            link_decoded = url_decode_basic(link)

            # (A) 폴더명 ./이미지/ -> ./images/
            # 상대경로/절대경로 섞여도 우선 문자열 레벨에서 처리
            link_decoded = link_decoded.replace("./이미지/", "./images/")
            link_decoded = link_decoded.replace("/이미지/", "/images/")

            # (B) image (n).png -> image_n.png
            # link_decoded 안에서 파일명만 바꿔주기
            link_decoded = re.sub(
                r"image\s*\((\d+)\)\.(png|jpg|jpeg|gif|webp)",
                lambda mm: f"image_{mm.group(1)}.{mm.group(2)}",
                link_decoded,
                flags=re.IGNORECASE
            )

            # 다시 링크에 공백 있으면 %20로 돌려놓기(마크다운 링크 안전)
            link_fixed = url_encode_spaces(link_decoded)
            return f"{prefix}{link_fixed}{suffix}"

        updated = MD_IMAGE_LINK_RE.sub(replace_link, updated)

        if updated != old:
            print(f"[MD] update links: {md}")
            safe_write_text(md, updated)

    print("\nDONE. Now run:")
    print("  git status")
    print("  git diff")
    print("  git commit -m \"chore: rename image paths to ascii and update md links\"")
    print("  git push")

if __name__ == "__main__":
    main()