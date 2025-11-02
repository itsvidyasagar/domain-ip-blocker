from tqdm import tqdm

def progress_bar(desc, current, total):
    if total <= 0:
        total = 1
    if current == 1:
        progress_bar.bar = tqdm(
            total=total,
            desc=desc,
            bar_format="{desc:<20} |{bar:20}| {percentage:5.1f}% | ETA: {remaining}s",
            colour="cyan",
        )
    progress_bar.bar.n = current
    progress_bar.bar.refresh()
    if current == total:
        progress_bar.bar.close()
