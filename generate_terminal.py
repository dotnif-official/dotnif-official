import gifos
from datetime import datetime
import os
import requests

USERNAME = (
    os.environ.get("GIT_USERNAME")
    or os.environ.get("GITHUB_REPOSITORY_OWNER")
    or "dotnif-official"
)

def get_total_repos(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            return response.json().get("public_repos", 0)
    except:
        pass
    return None

try:
    github_stats = gifos.utils.fetch_github_stats(user_name=USERNAME)
    has_stats = github_stats is not None
except Exception as e:
    print(f"Warning: Error fetching GitHub stats: {e}")
    has_stats = False
    github_stats = None

total_repos = get_total_repos(USERNAME)

t = gifos.Terminal(width=710, height=480, xpad=15, ypad=15)
t.set_prompt(f"\x1b[96m{USERNAME}\x1b[0m@\x1b[94marctic-edge\x1b[0m ~> ")

# Boot Sequence
t.gen_text("Booting DOTNIF_OS v2.4.0 [Arctic Pulse]...", row_num=1)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m Global Edge Network online (TTFB: 42ms)", row_num=2)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m Telemetry synchronized: 0.00 CLS / 100 Performance", row_num=3)
t.clone_frame(10)

t.gen_prompt(row_num=4)
t.gen_typing_text("neofetch --studio " + USERNAME, row_num=4, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=5)
t.gen_text("\x1b[96m=== DotNif Studio Profile ===\x1b[0m", row_num=6)
t.clone_frame(3)

if has_stats:
    repos_count = total_repos if total_repos else github_stats.total_repo_contributions
    stats_lines = [
        f"\x1b[94mStudio:\x1b[0m      {github_stats.account_name or 'DotNif'}",
        "\x1b[94mFocus:\x1b[0m       High-Performance Web & E-Commerce",
        f"\x1b[94mFollowers:\x1b[0m   {github_stats.total_followers}",
        f"\x1b[94mStars:\x1b[0m       {github_stats.total_stargazers}",
        f"\x1b[94mCommits:\x1b[0m     {github_stats.total_commits_last_year} (last year)",
        f"\x1b[94mPRs:\x1b[0m         {github_stats.total_pull_requests_made}",
        f"\x1b[94mRepos:\x1b[0m       {repos_count}",
        f"\x1b[94mRank:\x1b[0m        {github_stats.user_rank.level} ({github_stats.user_rank.percentile:.1f}%)",
    ]
    
    if github_stats.languages_sorted:
        top_langs = github_stats.languages_sorted[:3]
        langs_str = ", ".join([f"{lang[0]} ({lang[1]}%)" for lang in top_langs])
        stats_lines.append(f"\x1b[94mTop Langs:\x1b[0m   {langs_str}")
else:
    stats_lines = [
        f"\x1b[94mStudio:\x1b[0m      DotNif",
        "\x1b[94mFocus:\x1b[0m       High-Performance Web & E-Commerce",
        "\x1b[94mFollowers:\x1b[0m   --",
        "\x1b[94mStars:\x1b[0m       --",
        "\x1b[94mCommits:\x1b[0m     --",
        "\x1b[94mPRs:\x1b[0m         --",
        "\x1b[94mRepos:\x1b[0m       --",
        "\x1b[94mSLA:\x1b[0m         100% Code Ownership",
    ]

for i, line in enumerate(stats_lines):
    t.gen_text(line, row_num=7+i)
    t.clone_frame(3)

t.clone_frame(45)
t.gen_text("\x1b[96m=============================\x1b[0m", row_num=7+len(stats_lines))
t.clone_frame(25)

# Clear and Tech Stack
t.gen_prompt(row_num=8+len(stats_lines))
t.gen_typing_text("clear", row_num=8+len(stats_lines), contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat stack_matrix.json", row_num=1, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m=== DotNif Production Stack ===\x1b[0m", row_num=3)
t.clone_frame(3)

skills = [
    ("\x1b[94mModern Web:\x1b[0m     ", "Next.js 16, React 19, TypeScript, Turbopack"),
    ("\x1b[94mStyling & UI:\x1b[0m   ", "Tailwind CSS v4, GSAP Motion, Figma"),
    ("\x1b[94mCMS & Commerce:\x1b[0m ", "WordPress, WooCommerce, Headless Mesh"),
    ("\x1b[94mInfrastructure:\x1b[0m ", "Vercel Edge SSR, Cloudflare, GitHub CI/CD"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(45)
t.gen_text("\x1b[96m===============================\x1b[0m", row_num=4+len(skills))
t.clone_frame(25)

# Final message
final_row = 5 + len(skills)
t.gen_prompt(row_num=final_row)
t.gen_typing_text("echo 'DotNif — Built for velocity, engineered for conversion.'", row_num=final_row, contin=True, speed=1)
t.clone_frame(5)
t.gen_text("\x1b[96mDotNif — Built for velocity, engineered for conversion.\x1b[0m", row_num=final_row+1)
t.clone_frame(120)

# Save to terminal.gif
t.gen_gif()
if os.path.exists("output.gif"):
    if os.path.exists("terminal.gif"):
        os.remove("terminal.gif")
    os.rename("output.gif", "terminal.gif")
