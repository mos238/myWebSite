#!/bin/bash
# ============================================================================
# Fast Video Downloader - Optimized with parallel downloads
# Supports playlists, mixes, and single videos
# Uses cookies.txt directly with yt-dlp
# ============================================================================

# Configuration
COOKIE_FILE="/home/zeus/9370/cookies/ph_cookies.txt"
SCRIPT_NAME="fast-dl.sh"
SCRIPT_PATH="/home/zeus/$SCRIPT_NAME"
VERSION="2.0.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================

print_color() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo -e "\n${CYAN}======================================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}======================================================================${NC}"
}

print_error() {
    print_color "$RED" "$1"
}

print_success() {
    print_color "$GREEN" "$1"
}

print_warning() {
    print_color "$YELLOW" "$1"
}

print_info() {
    print_color "$BLUE" "$1"
}

check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        print_error "❌ $1 is not installed!"
        return 1
    fi
    return 0
}

# Get default downloads directory based on XDG or fallback
get_default_downloads_dir() {
    # Try XDG_DOWNLOAD_DIR first
    if [[ -n "$XDG_DOWNLOAD_DIR" && -d "$XDG_DOWNLOAD_DIR" ]]; then
        echo "$XDG_DOWNLOAD_DIR"
    # Try user's Downloads folder
    elif [[ -d "$HOME/Downloads" ]]; then
        echo "$HOME/Downloads"
    # Try language-specific Downloads folders
    elif [[ -d "$HOME/Загрузки" ]]; then  # Russian
        echo "$HOME/Загрузки"
    elif [[ -d "$HOME/Descargas" ]]; then  # Spanish
        echo "$HOME/Descargas"
    elif [[ -d "$HOME/Téléchargements" ]]; then  # French
        echo "$HOME/Téléchargements"
    elif [[ -d "$HOME/ダウンロード" ]]; then  # Japanese
        echo "$HOME/ダウンロード"
    elif [[ -d "$HOME/下載" ]]; then  # Traditional Chinese
        echo "$HOME/下載"
    elif [[ -d "$HOME/下载" ]]; then  # Simplified Chinese
        echo "$HOME/下载"
    # Fallback to current directory with downloads subfolder
    else
        echo "$PWD/downloads"
    fi
}

# Check if URL is a playlist/mix
is_playlist_url() {
    local url="$1"
    # Check for playlist indicators in URL
    if [[ "$url" =~ [\&\?]list= ]] || \
       [[ "$url" =~ /playlist/ ]] || \
       [[ "$url" =~ /mix/ ]] || \
       [[ "$url" =~ \&mix= ]] || \
       [[ "$url" =~ /channel/ ]] || \
       [[ "$url" =~ /c/ ]] || \
       [[ "$url" =~ /user/ ]]; then
        return 0
    fi
    return 1
}

# Get playlist information
get_playlist_info() {
    local url="$1"
    
    print_header "Playlist Information"
    echo "🔗 URL: $url"
    
    # Get playlist info using yt-dlp
    local playlist_title
    playlist_title=$(yt-dlp --cookies "$COOKIE_FILE" --flat-playlist --print "%(playlist_title)s" "$url" 2>/dev/null | head -1)
    
    local video_count
    video_count=$(yt-dlp --cookies "$COOKIE_FILE" --flat-playlist --print "%(playlist_count)s" "$url" 2>/dev/null | head -1)
    
    if [[ -n "$playlist_title" ]]; then
        echo "📝 Playlist Title: $playlist_title"
    fi
    
    if [[ -n "$video_count" && "$video_count" -gt 0 ]]; then
        echo "🎬 Total Videos: $video_count"
    else
        # Alternative method to count
        video_count=$(yt-dlp --cookies "$COOKIE_FILE" --flat-playlist --dump-json "$url" 2>/dev/null | grep -c '"id"' || echo "Unknown")
        if [[ "$video_count" != "Unknown" ]]; then
            echo "🎬 Total Videos: $video_count"
        fi
    fi
}

# ============================================================================
# Main Functions
# ============================================================================

check_cookie_file() {
    if [[ ! -f "$COOKIE_FILE" ]]; then
        print_error "❌ Cookie file not found: $COOKIE_FILE"
        echo "   To create cookies.txt:"
        echo "   1. Install 'cookies.txt' browser extension"
        echo "   2. Export cookies from your browser"
        echo "   3. Save to: $COOKIE_FILE"
        return 1
    fi
    
    local size
    size=$(wc -c < "$COOKIE_FILE" 2>/dev/null || echo "0")
    
    if [[ $size -lt 100 ]]; then
        print_warning "⚠️  Cookie file is very small ($size bytes)"
        echo "   It might not contain valid cookies"
    fi
    
    if head -n 1 "$COOKIE_FILE" 2>/dev/null | grep -q "^# Netscape"; then
        echo "✅ Cookie file format: Netscape"
    elif head -n 1 "$COOKIE_FILE" 2>/dev/null | grep -q "# HTTP Cookie File"; then
        echo "✅ Cookie file format: HTTP Cookie"
    else
        echo "✅ Cookie file found ($size bytes)"
    fi
    
    return 0
}

run_playlist_download() {
    local url="$1"
    local output_dir="$2"
    local format="$3"
    local parallel="$4"
    local threads="$5"
    local max_videos="$6"
    local playlist_start="$7"
    local playlist_end="$8"
    local reverse="$9"
    
    print_header "Downloading Playlist/Mix"
    echo "🔗 URL: $url"
    echo "📁 Output: $output_dir"
    echo "🍪 Cookies: $COOKIE_FILE"
    echo "⚡ Parallel: $([ "$parallel" = "true" ] && echo "Yes ($threads threads)" || echo "No")"
    [[ -n "$max_videos" && "$max_videos" -gt 0 ]] && echo "🎯 Max videos: $max_videos"
    [[ -n "$playlist_start" && "$playlist_start" -gt 0 ]] && echo "▶️  Start at: $playlist_start"
    [[ -n "$playlist_end" && "$playlist_end" -gt 0 ]] && echo "⏸️  End at: $playlist_end"
    
    # Create playlist subdirectory
    local playlist_name
    playlist_name=$(yt-dlp --cookies "$COOKIE_FILE" --flat-playlist --print "%(playlist_title)s" "$url" 2>/dev/null | \
                    head -1 | sed 's/[\/:*?"<>|]/_/g')
    
    if [[ -z "$playlist_name" ]]; then
        playlist_name="playlist_$(date +%Y%m%d_%H%M%S)"
    fi
    
    local playlist_dir="${output_dir}/${playlist_name}"
    mkdir -p "$playlist_dir"
    
    print_info "📁 Playlist directory: $playlist_dir"
    
    # Build yt-dlp command for playlist
    local cmd=(
        "yt-dlp"
        "--cookies" "$COOKIE_FILE"
        "--output" "$playlist_dir/%(playlist_index)s - %(title)s [%(id)s].%(ext)s"
        "--format" "$format"
        "--merge-output-format" "mp4"
        "--yes-playlist"
        "--progress"
        "--console-title"
        "--user-agent" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "--throttled-rate" "5M"
        "--retries" "10"
        "--fragment-retries" "10"
        "--file-access-retries" "3"
        "--limit-rate" "10M"
        "--socket-timeout" "30"
        "--source-address" "0.0.0.0"
        "--embed-thumbnail"
        "--add-metadata"
    )
    
    # Add parallel fragment downloads
    if [[ "$parallel" = "true" ]]; then
        cmd+=("--concurrent-fragments" "$threads")
    else
        cmd+=("--concurrent-fragments" "1")
    fi
    
    # Add playlist range options
    if [[ -n "$max_videos" && "$max_videos" -gt 0 ]]; then
        cmd+=("--playlist-end" "$max_videos")
    fi
    
    if [[ -n "$playlist_start" && "$playlist_start" -gt 0 ]]; then
        cmd+=("--playlist-start" "$playlist_start")
    fi
    
    if [[ -n "$playlist_end" && "$playlist_end" -gt 0 ]]; then
        cmd+=("--playlist-end" "$playlist_end")
    fi
    
    if [[ "$reverse" = "true" ]]; then
        cmd+=("--playlist-reverse")
    fi
    
    cmd+=("$url")
    
    # Execute download
    local start_time
    start_time=$(date +%s)
    
    if "${cmd[@]}"; then
        local end_time elapsed
        end_time=$(date +%s)
        elapsed=$((end_time - start_time))
        
        # Count downloaded files
        local file_count
        file_count=$(find "$playlist_dir" -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \) 2>/dev/null | wc -l)
        
        print_success "\n✅ Playlist download completed in ${elapsed} seconds!"
        print_success "📊 Downloaded: $file_count videos"
        print_success "📁 Saved to: $playlist_dir"
        return 0
    else
        print_error "\n❌ Playlist download failed!"
        return 1
    fi
}

run_single_download() {
    local url="$1"
    local output_dir="$2"
    local format="$3"
    local parallel="$4"
    local threads="$5"
    
    print_header "Starting Download"
    echo "🔗 URL: $(echo "$url" | cut -c1-50)..."
    echo "📁 Output: $output_dir"
    echo "🍪 Cookies: $COOKIE_FILE"
    echo "⚡ Parallel: $([ "$parallel" = "true" ] && echo "Yes ($threads threads)" || echo "No")"
    
    # Build yt-dlp command
    local cmd=(
        "yt-dlp"
        "--cookies" "$COOKIE_FILE"
        "--output" "$output_dir/%(title)s [%(id)s].%(ext)s"
        "--format" "$format"
        "--merge-output-format" "mp4"
        "--no-playlist"
        "--progress"
        "--console-title"
        "--user-agent" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "--throttled-rate" "5M"
        "--retries" "10"
        "--fragment-retries" "10"
        "--file-access-retries" "3"
        "--limit-rate" "10M"
        "--socket-timeout" "30"
        "--source-address" "0.0.0.0"
        "--embed-thumbnail"
        "--add-metadata"
    )
    
    if [[ "$parallel" = "true" ]]; then
        cmd+=("--concurrent-fragments" "$threads")
    else
        cmd+=("--concurrent-fragments" "1")
    fi
    
    cmd+=("$url")
    
    # Execute download
    local start_time
    start_time=$(date +%s)
    
    if "${cmd[@]}"; then
        local end_time elapsed
        end_time=$(date +%s)
        elapsed=$((end_time - start_time))
        
        # Get the downloaded file
        local latest_file
        latest_file=$(find "$output_dir" -maxdepth 1 -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \) 2>/dev/null | sort -r | head -n1)
        
        if [[ -n "$latest_file" ]]; then
            local file_size
            file_size=$(du -h "$latest_file" 2>/dev/null | cut -f1)
            print_success "\n✅ Download completed in ${elapsed} seconds!"
            print_success "📁 File: $(basename "$latest_file")"
            print_success "📊 Size: $file_size"
        else
            print_success "\n✅ Download completed in ${elapsed} seconds!"
        fi
        return 0
    else
        print_error "\n❌ Download failed!"
        return 1
    fi
}

get_video_info() {
    local url="$1"
    
    if is_playlist_url "$url"; then
        get_playlist_info "$url"
        return
    fi
    
    print_header "Video Information"
    echo "🔗 URL: $(echo "$url" | cut -c1-50)..."
    
    yt-dlp --cookies "$COOKIE_FILE" --skip-download --dump-json --no-playlist "$url" 2>/dev/null | \
        python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'📝 Title: {data.get(\"title\", \"Unknown\")}')
    print(f'⏱️  Duration: {data.get(\"duration\", 0)} seconds')
    print(f'👤 Uploader: {data.get(\"uploader\", \"Unknown\")}')
    print(f'👁️  Views: {data.get(\"view_count\", 0):,}')
    print(f'📅 Upload date: {data.get(\"upload_date\", \"Unknown\")}')
    print(f'🎬 Resolution: {data.get(\"height\", \"Unknown\")}p')
except Exception as e:
    print('❌ Failed to get video information')
"
}

list_formats() {
    local url="$1"
    
    print_header "Available Formats"
    echo "🔗 URL: $(echo "$url" | cut -c1-50)..."
    echo ""
    
    yt-dlp --cookies "$COOKIE_FILE" --list-formats "$url"
}

batch_download() {
    local urls_file="$1"
    local output_dir="$2"
    local parallel_downloads="$3"
    local parallel_fragments="$4"
    
    if [[ ! -f "$urls_file" ]]; then
        print_error "❌ URLs file not found: $urls_file"
        return 1
    fi
    
    local url_count
    url_count=$(wc -l < "$urls_file")
    
    print_header "Batch Download"
    echo "📄 URLs file: $urls_file"
    echo "📦 Total items: $url_count"
    echo "📁 Output: $output_dir"
    echo "⚡ Parallel downloads: $parallel_downloads"
    echo "⚡ Parallel fragments: $parallel_fragments"
    
    # Create a subdirectory for batch downloads
    local batch_dir="${output_dir}/batch_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$batch_dir"
    
    # Read URLs into array
    mapfile -t urls < "$urls_file"
    
    local success_count=0
    local fail_count=0
    local total=${#urls[@]}
    
    # Function to download a single URL
    download_single() {
        local url="$1"
        local idx="$2"
        
        echo -e "\n${CYAN}======================================================================${NC}"
        echo "📥 Downloading [$((idx+1))/$total]: $(echo "$url" | cut -c1-50)..."
        
        # Check if it's a playlist
        if is_playlist_url "$url"; then
            yt-dlp \
                --cookies "$COOKIE_FILE" \
                --output "$batch_dir/%(playlist_title)s/%(playlist_index)s - %(title)s [%(id)s].%(ext)s" \
                --format "best[height<=1080]/best" \
                --merge-output-format "mp4" \
                --yes-playlist \
                --progress \
                --concurrent-fragments "$parallel_fragments" \
                --retries 5 \
                "$url" > /dev/null 2>&1
        else
            yt-dlp \
                --cookies "$COOKIE_FILE" \
                --output "$batch_dir/%(title)s [%(id)s].%(ext)s" \
                --format "best[height<=1080]/best" \
                --merge-output-format "mp4" \
                --no-playlist \
                --progress \
                --concurrent-fragments "$parallel_fragments" \
                --retries 5 \
                "$url" > /dev/null 2>&1
        fi
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully downloaded"
            return 0
        else
            echo "❌ Failed to download"
            return 1
        fi
    }
    
    # Export function for parallel execution
    export -f download_single is_playlist_url
    export COOKIE_FILE
    export batch_dir
    export parallel_fragments
    export total
    export CYAN
    export NC
    
    # Download URLs in parallel
    local pids=()
    for ((i=0; i<total; i++)); do
        download_single "${urls[$i]}" "$i" &
        pids+=($!)
        
        # Wait if we've reached parallel_downloads limit
        if [[ ${#pids[@]} -ge $parallel_downloads ]]; then
            wait "${pids[0]}"
            # Check exit status and update counters
            if [[ $? -eq 0 ]]; then
                ((success_count++))
            else
                ((fail_count++))
            fi
            # Remove first pid from array
            pids=("${pids[@]:1}")
        fi
    done
    
    # Wait for remaining downloads
    for pid in "${pids[@]}"; do
        wait "$pid"
        if [[ $? -eq 0 ]]; then
            ((success_count++))
        else
            ((fail_count++))
        fi
    done
    
    print_header "Batch Download Complete"
    echo "📊 Results:"
    echo "   ✅ Success: $success_count"
    echo "   ❌ Failed: $fail_count"
    echo "   📊 Total: $total"
    echo "   📁 Saved to: $batch_dir"
    
    return $((fail_count > 0))
}

prompt_for_url() {
    # Get default downloads directory
    local default_downloads
    default_downloads=$(get_default_downloads_dir)
    
    print_header "🚀 FAST VIDEO DOWNLOADER v${VERSION}"
    echo "📍 Script location: $SCRIPT_PATH"
    echo "🍪 Cookie file: $COOKIE_FILE"
    echo "📁 Default download folder: $default_downloads"
    echo "🎵 Supports: Videos, Playlists, Mixes, Channels"
    echo ""
    
    while true; do
        read -rp "🔗 Enter URL (video/playlist/mix) or 'q' to quit: " url
        
        if [[ "$url" == "q" ]] || [[ "$url" == "quit" ]]; then
            echo "👋 Exiting..."
            exit 0
        fi
        
        if [[ -n "$url" ]]; then
            break
        fi
        
        print_warning "⚠️  Please enter a valid URL or 'q' to quit"
    done
    
    # Check if it's a playlist
    local is_playlist=false
    if is_playlist_url "$url"; then
        is_playlist=true
        print_info "\n📋 Playlist/Mix detected!"
        get_playlist_info "$url"
        echo ""
    fi
    
    # Ask for parallel download
    read -rp "⚡ Enable parallel downloads? (y/N): " parallel_input
    parallel_input=${parallel_input:-n}
    
    # Ask for quality
    read -rp "🎬 Quality (1080p/720p/480p/best/worst) [1080p]: " format_choice
    format_choice=${format_choice:-1080p}
    
    # Map format choices
    local format
    case "$format_choice" in
        1080p) format="best[height<=1080]/best" ;;
        720p) format="best[height<=720]/best" ;;
        480p) format="best[height<=480]/best" ;;
        best) format="best" ;;
        worst) format="worst" ;;
        *) format="best[height<=1080]/best" ;;
    esac
    
    # Ask for output directory
    read -rp "📁 Output directory [$default_downloads]: " custom_output
    custom_output=${custom_output:-$default_downloads}
    
    # Create output directory if it doesn't exist
    mkdir -p "$custom_output"
    
    # Playlist-specific options
    local max_videos=""
    local playlist_start=""
    local playlist_end=""
    local reverse="false"
    
    if [[ "$is_playlist" == true ]]; then
        echo ""
        print_info "Playlist Options:"
        read -rp "   Max number of videos to download (press Enter for all): " max_videos
        read -rp "   Start from video number (press Enter for first): " playlist_start
        read -rp "   End at video number (press Enter for last): " playlist_end
        read -rp "   Download in reverse order? (y/N): " reverse_input
        if [[ "${reverse_input,,}" == "y" ]]; then
            reverse="true"
        fi
    fi
    
    echo ""
    # Run download
    if [[ "$is_playlist" == true ]]; then
        if [[ "${parallel_input,,}" == "y" ]]; then
            run_playlist_download "$url" "$custom_output" "$format" "true" 4 "$max_videos" "$playlist_start" "$playlist_end" "$reverse"
        else
            run_playlist_download "$url" "$custom_output" "$format" "false" 1 "$max_videos" "$playlist_start" "$playlist_end" "$reverse"
        fi
    else
        if [[ "${parallel_input,,}" == "y" ]]; then
            run_single_download "$url" "$custom_output" "$format" "true" 4
        else
            run_single_download "$url" "$custom_output" "$format" "false" 1
        fi
    fi
    
    # Ask if user wants to download another video
    echo ""
    read -rp "📥 Download another video/playlist? (y/N): " another
    if [[ "${another,,}" == "y" ]]; then
        echo ""
        prompt_for_url
    fi
}

show_help() {
    cat << EOF

${CYAN}Fast Video Downloader ${VERSION}${NC}
Optimized video/playlist downloader using yt-dlp with cookie support

${YELLOW}Script location:${NC} $SCRIPT_PATH
${YELLOW}Cookie file:${NC} $COOKIE_FILE

${GREEN}Usage:${NC}
  fast-dl [OPTIONS] [URL...]
  $SCRIPT_NAME [OPTIONS] [URL...]

${GREEN}Options:${NC}
  -h, --help            Show this help message
  -i, --info URL        Show video/playlist information without downloading
  -F, --list-formats URL List available formats for video
  -o, --output DIR      Output directory (default: user's Downloads folder)
  -f, --format FORMAT   Video format (default: best[height<=1080]/best)
  -p, --parallel        Enable parallel fragment downloads
  -t, --threads N       Number of parallel threads (default: 4)
  -b, --batch FILE      Download multiple URLs from file in parallel
  --batch-threads N     Parallel downloads for batch mode (default: 2)
  
${GREEN}Playlist Options:${NC}
  --playlist            Force playlist mode (even for single videos)
  --no-playlist         Force single video mode (even for playlists)
  --max-videos N        Maximum number of videos to download from playlist
  --playlist-start N    First video to download (default: 1)
  --playlist-end N      Last video to download
  --reverse             Download playlist in reverse order

${GREEN}Interactive Mode:${NC}
  If no URL is provided, the script will prompt for one interactively.

${GREEN}Examples:${NC}
  $SCRIPT_NAME                           # Interactive mode
  $SCRIPT_NAME https://example.com/video # Direct download
  $SCRIPT_NAME -p -t 8 https://example.com/video
  $SCRIPT_NAME https://youtube.com/playlist?list=xxx  # Download playlist
  $SCRIPT_NAME --max-videos 10 https://youtube.com/playlist?list=xxx
  $SCRIPT_NAME --playlist-start 5 --playlist-end 15 https://youtube.com/playlist?list=xxx
  $SCRIPT_NAME -b urls.txt
  $SCRIPT_NAME --info https://example.com/playlist
  $SCRIPT_NAME --list-formats https://example.com/video

${GREEN}Format Examples:${NC}
  best[height<=1080]/best  # 1080p or lower (default)
  best[height<=720]/best   # 720p or lower
  best                     # Best available quality
  worst                    # Worst quality
  22/18/best               # Specific format IDs

EOF
}

# ============================================================================
# Main Script
# ============================================================================

main() {
    # Default values - use user's default downloads directory
    local default_downloads
    default_downloads=$(get_default_downloads_dir)
    
    local urls=()
    local output_dir="$default_downloads"
    local format="best[height<=1080]/best"
    local parallel=false
    local threads=4
    local batch_file=""
    local batch_threads=2
    local show_info=false
    local list_formats=false
    local force_playlist=false
    local force_no_playlist=false
    local max_videos=""
    local playlist_start=""
    local playlist_end=""
    local reverse=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--info)
                show_info=true
                if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                    urls+=("$2")
                    shift
                fi
                ;;
            -F|--list-formats)
                list_formats=true
                if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                    urls+=("$2")
                    shift
                fi
                ;;
            -o|--output)
                output_dir="$2"
                shift
                ;;
            -f|--format)
                format="$2"
                shift
                ;;
            -p|--parallel)
                parallel=true
                ;;
            -t|--threads)
                threads="$2"
                shift
                ;;
            -b|--batch)
                batch_file="$2"
                shift
                ;;
            --batch-threads)
                batch_threads="$2"
                shift
                ;;
            --playlist)
                force_playlist=true
                ;;
            --no-playlist)
                force_no_playlist=true
                ;;
            --max-videos)
                max_videos="$2"
                shift
                ;;
            --playlist-start)
                playlist_start="$2"
                shift
                ;;
            --playlist-end)
                playlist_end="$2"
                shift
                ;;
            --reverse)
                reverse=true
                ;;
            *)
                if [[ ! "$1" =~ ^- ]]; then
                    urls+=("$1")
                else
                    print_error "Unknown option: $1"
                    show_help
                    exit 1
                fi
                ;;
        esac
        shift
    done
    
    # Check dependencies
    if ! check_dependency "yt-dlp"; then
        echo "Install with: pip install yt-dlp"
        exit 1
    fi
    
    if ! check_dependency "python3"; then
        print_error "Python 3 is required"
        exit 1
    fi
    
    # Check cookie file
    if ! check_cookie_file; then
        exit 1
    fi
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # If no arguments provided (no URLs and no batch file), go to interactive mode
    if [[ ${#urls[@]} -eq 0 && -z "$batch_file" && "$show_info" = false && "$list_formats" = false ]]; then
        prompt_for_url
        exit $?
    fi
    
    # Show video information
    if [[ "$show_info" = true && ${#urls[@]} -gt 0 ]]; then
        get_video_info "${urls[0]}"
        exit 0
    fi
    
    # List formats
    if [[ "$list_formats" = true && ${#urls[@]} -gt 0 ]]; then
        list_formats "${urls[0]}"
        exit 0
    fi
    
    # Batch download mode
    if [[ -n "$batch_file" ]]; then
        batch_download "$batch_file" "$output_dir" "$batch_threads" "$threads"
        exit $?
    fi
    
    # Single download mode(s)
    local all_success=true
    
    for url in "${urls[@]}"; do
        # Determine if it's a playlist
        local is_playlist=false
        if [[ "$force_playlist" == true ]]; then
            is_playlist=true
        elif [[ "$force_no_playlist" == false ]] && is_playlist_url "$url"; then
            is_playlist=true
        fi
        
        if [[ "$is_playlist" == true ]]; then
            if ! run_playlist_download "$url" "$output_dir" "$format" "$parallel" "$threads" "$max_videos" "$playlist_start" "$playlist_end" "$reverse"; then
                all_success=false
                print_error "\n❌ Failed to download playlist: $(echo "$url" | cut -c1-50)..."
            fi
        else
            if ! run_single_download "$url" "$output_dir" "$format" "$parallel" "$threads"; then
                all_success=false
                print_error "\n❌ Failed to download: $(echo "$url" | cut -c1-50)..."
                echo "💡 Try: --format worst (for compatibility)"
                echo "💡 Try without --parallel"
            fi
        fi
    done
    
    if [[ "$all_success" = true ]]; then
        print_success "\n📁 All downloads saved to: $(realpath "$output_dir")"
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"