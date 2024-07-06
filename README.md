# TikTok Trending Videos Processing Pipeline

This project fetches, modifies, and reports on 100 trending TikTok videos from your specified location.

`TikTokApi==6.2.0` `ffmpeg==1.4` `playwright==1.30.0`

## Setup

**Environmental Variables**:
   - Ensure you have set `ms_token` in your environment for API access/authentication.



### Settings Explanation

```python
# Token
ms_token = os.environ.get("ms_token", None)
```
- **ms_token**: This variable retrieves the value of `ms_token` from your environment variables. It's crucial for authentication or API access within your script.

*Get your own ms_token from your cookies on [tiktok.com](https://tiktok.com)
### Paths Definition

```python
# Define paths
output_folder = r'<output_folder>'
audio = r'<audio>.mp3'
report = r'REPORT.md'
```
- **output_folder**: Specifies the directory where processed videos will be saved. Adjust this path to suit your local environment.
  
- **audio**: Points to the location of the audio file that will replace the soundtracks of the TikTok videos.
  
- **report**: Specifies the file path for the Markdown report (`REPORT.md`) summarizing the processing pipeline's activities.

### Ratios for Modifications

```python
# Define ratios
speed_ratio_int = 0.9
resize_ratio_int = 0.9
```
- **speed_ratio_int**: Specifies the speed reduction ratio (90%) for modifying the video speed.
  
- **resize_ratio_int**: Defines the resize ratio (90%) for reducing the video resolution.

## Usage

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd tiktok-processing-pipeline
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Report

Check `REPORT.md` for a summary of the processing pipeline's activities.

## Issues

If you encounter any issues, please [open an issue](https://github.com/hinderss/tiktok-processing-pipeline/issues) on GitHub.
