import imageio
import os

def process_all_mp4_with_walk_and_progress():
    mp4_files = []
    # 用os.walk递归查找所有mp4文件
    for root, dirs, files in os.walk("examples/1"):
        for f in files:
            if f.lower().endswith(".mp4"):
                mp4_files.append(os.path.join(root, f))

    total = len(mp4_files)
    if total == 0:
        print("未找到任何mp4文件。")
        return

    for idx, filepath in enumerate(mp4_files, 1):
        print(f"正在处理({idx}/{total}): {filepath}")
        try:
            reader = imageio.get_reader(filepath)
            fps = reader.get_meta_data().get('fps', 30)
            frames = []
            for frame in reader:
                frames.append(frame)
            reader.close()

            writer = imageio.get_writer(filepath, fps=fps)
            for frame in frames:
                writer.append_data(frame)
            writer.close()
        except Exception as e:
            print(f"处理文件时出错: {filepath}, 错误信息: {e}")

if __name__ == "__main__":
    process_all_mp4_with_walk_and_progress()

# import imageio

# def remove_last_n_frames_from_mp4(mp4_path, n_remove=5):
#     # 读取视频所有帧
#     reader = imageio.get_reader(mp4_path)
#     fps = reader.get_meta_data().get('fps', 30)
#     frames = [frame for frame in reader]
#     reader.close()

#     # 去掉最后n_remove帧
#     if len(frames) > n_remove:
#         frames_to_write = frames[:-n_remove]
#     else:
#         print(f"视频帧数少于等于{n_remove}，不做处理。")
#         return

#     # 重新写入
#     writer = imageio.get_writer(mp4_path, fps=fps)
#     for frame in frames_to_write:
#         writer.append_data(frame)
#     writer.close()
#     print(f"已从{mp4_path}中移除最后{n_remove}帧。")

# if __name__ == "__main__":
#     mp4_file = r"C:\Users\15275\Documents\GitHub\StereoWorld\examples\5.mp4"
#     remove_last_n_frames_from_mp4(mp4_file, n_remove=5)


# import os
# import imageio
# import numpy as np

# def crop_black_borders_bounds(frame, black_thresh=15, min_content_row_ratio=0.1):
#     """
#     返回裁剪后的上下边界（top, bottom），不直接裁剪frame
#     """
#     gray = np.mean(frame, axis=2)
#     row_means = np.mean(gray, axis=1)
#     is_black_row = row_means < black_thresh

#     # 从上向下第一个非黑行
#     top = 0
#     while top < len(is_black_row) and is_black_row[top]:
#         top += 1
#     # 从下向上第一个非黑行
#     bottom = len(is_black_row) - 1
#     while bottom >= 0 and is_black_row[bottom]:
#         bottom -= 1

#     total_rows = len(is_black_row)
#     min_content = int(total_rows * min_content_row_ratio)
#     if bottom - top + 1 < min_content:
#         # 保守返回不裁剪
#         return 0, frame.shape[0] - 1

#     return top, bottom

# def process_video_remove_black_borders(video_path):
#     """
#     处理指定视频文件，去除上下黑边，保存回原文件
#     解决所有帧尺寸必须相同的问题：统一所有帧的裁剪区域
#     """
#     ext = os.path.splitext(video_path)[1].lower()
#     video_exts = {'.mp4', '.avi', '.mov', '.mkv'}
#     if ext not in video_exts:
#         print(f"不支持的视频格式: {video_path}")
#         return

#     try:
#         print(f"处理: {video_path}")
#         reader = imageio.get_reader(video_path)
#         fps = reader.get_meta_data().get('fps', 30)

#         # --- Pass 1: 找所有帧中的“最大裁剪范围” ---
#         top_list = []
#         bottom_list = []
#         frames = []
#         for i, frame in enumerate(reader):
#             t, b = crop_black_borders_bounds(frame)
#             top_list.append(t)
#             bottom_list.append(b)
#             frames.append(frame)
#         reader.close()

#         # 为了保证所有帧裁剪后shape一致，取max(top)和min(bottom)
#         crop_top = max(top_list)
#         crop_bottom = min(bottom_list)
#         # 容错：若不裁/无效，回退全frame
#         if crop_bottom < crop_top or (crop_bottom - crop_top + 1) < int(frames[0].shape[0] * 0.1):
#             crop_top = 0
#             crop_bottom = frames[0].shape[0] - 1

#         crop_slice = slice(crop_top, crop_bottom + 1)

#         # --- Pass 2: 实际裁剪所有帧 ---
#         out_frames = []
#         for f in frames:
#             out_frames.append(f[crop_slice, :, :])

#         # 使用临时文件避免写坏
#         tmp_fpath = video_path + ".noborder.tmp.mp4"
#         writer = imageio.get_writer(tmp_fpath, fps=fps)
#         for f in out_frames:
#             writer.append_data(f)
#         writer.close()

#         os.replace(tmp_fpath, video_path)
#         print(f"已裁剪并覆盖: {video_path}")
#         print(f"统一裁剪范围: rows {crop_top}~{crop_bottom} (orig: {frames[0].shape[0]})")
#     except Exception as e:
#         print(f"处理出错: {video_path}, 错误: {e}")

# if __name__ == "__main__":
#     import os

#     video_folder = "./GenStereo/select3"
#     video_exts = {'.mp4', '.avi', '.mov', '.mkv'}

#     for root, dirs, files in os.walk(video_folder):
#         for fname in files:
#             ext = os.path.splitext(fname)[1].lower()
#             if ext in video_exts:
#                 video_path = os.path.join(root, fname)
#                 process_video_remove_black_borders(video_path)
