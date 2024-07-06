from time import time


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def generate_markdown_report(num_videos, time_taken, exceptions, file_path):
    report = f"# Trending TikTok Videos Report\n\n"
    report += f"A short report summarizing the actions performed.\n"
    report += f"## Number of videos processed: \n`{num_videos}`\n"
    report += f"## Time taken for the entire process: \n`{time_taken:.2f}` seconds\n"

    if exceptions:
        report += "## Exceptions:\n\n"
        for idx, exc in enumerate(exceptions, 1):
            report += f"{idx}. {exc}\n"
        report += "\n"

    try:
        with open(file_path, 'w') as file:
            file.write(report)
        print(f"Markdown report saved successfully to '{file_path}'.")
    except IOError as e:
        print(f"Error saving report to '{file_path}': {e}")

