from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agents.analytics_agent import AnalyticsAgent
from agents.promotion_agent import PromotionAgent
from agents.seo_agent import SEOAgent, SEOInput
from agents.shorts_agent import ShortsAgent
from youtube_api.client import YouTubeClient

console = Console()
ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)


def setup(_: argparse.Namespace) -> None:
    console.print(Panel.fit("OAuth setup. A browser window may open. Keep client_secret.json local."))
    yt = YouTubeClient()
    channel = yt.my_channel()
    console.print(f"Connected channel: [bold]{channel['snippet']['title']}[/bold]")


def channel(_: argparse.Namespace) -> None:
    yt = YouTubeClient()
    ch = yt.my_channel()
    stats = ch.get("statistics", {})
    table = Table(title="Channel")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Title", ch["snippet"].get("title", ""))
    table.add_row("Subscribers", stats.get("subscriberCount", "hidden"))
    table.add_row("Views", stats.get("viewCount", ""))
    table.add_row("Videos", stats.get("videoCount", ""))
    console.print(table)


def videos(args: argparse.Namespace) -> None:
    yt = YouTubeClient()
    vids = yt.recent_videos(max_results=args.max)
    table = Table(title="Recent Videos")
    table.add_column("Title")
    table.add_column("Views")
    table.add_column("Likes")
    table.add_column("Comments")
    for v in vids:
        table.add_row(
            v["snippet"].get("title", ""),
            v.get("statistics", {}).get("viewCount", "0"),
            v.get("statistics", {}).get("likeCount", "0"),
            v.get("statistics", {}).get("commentCount", "0"),
        )
    console.print(table)


def analytics(args: argparse.Namespace) -> None:
    yt = YouTubeClient()
    report = yt.analytics_summary(days=args.days)
    advice = AnalyticsAgent().recommend_from_summary(report)
    console.print(Panel("\n".join(advice), title=f"Analytics recommendations {report['start']} → {report['end']}"))


def campaign(args: argparse.Namespace) -> None:
    data = build_campaign(args.title, args.genre, args.mood, args.audience)
    path = save_markdown(data, f"campaign_{safe_name(args.title)}.md")
    console.print(Panel(f"Campaign generated: {path}", title="Done"))
    console.print(data["markdown"])


def report(args: argparse.Namespace) -> None:
    yt = YouTubeClient()
    ch = yt.my_channel()
    vids = yt.recent_videos(max_results=5)
    analytics_report = yt.analytics_summary(days=args.days)
    recommendations = AnalyticsAgent().recommend_from_summary(analytics_report)

    lines = [
        f"# BANG IT UP MUSIC — Growth Report\n",
        f"Channel: {ch['snippet'].get('title','')}\n",
        f"Period: {analytics_report['start']} → {analytics_report['end']}\n",
        "## Recommendations\n",
    ]
    lines += [f"- {x}" for x in recommendations]
    lines += ["\n## Recent videos\n"]
    for v in vids:
        stats = v.get("statistics", {})
        title = v["snippet"].get("title", "")
        lines.append(f"- {title}: {stats.get('viewCount','0')} views, {stats.get('likeCount','0')} likes")
    lines += ["\n## Weekly plan\n"]
    lines += [f"- {x}" for x in PromotionAgent().weekly_plan()]

    path = OUTPUTS / "growth_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    console.print(Panel(f"Saved report: {path}", title="Done"))


def build_campaign(title: str, genre: str, mood: str, audience: str) -> dict[str, Any]:
    seo = SEOAgent().generate(SEOInput(title=title, genre=genre, mood=mood, audience=audience))
    shorts = ShortsAgent().generate(title, genre, mood)
    posts = PromotionAgent().social_posts(title)
    plan = PromotionAgent().weekly_plan()

    md = [f"# Campaign: {title}\n", "## SEO Titles"]
    md += [f"- {t}" for t in seo["titles"]]
    md += ["\n## Description", str(seo["description"])]
    md += ["\n## Hashtags", " ".join(seo["hashtags"])]
    md += ["\n## Tags", ", ".join(seo["tags"])]
    md += ["\n## Pinned Comment", str(seo["pinned_comment"])]
    md += ["\n## Shorts Ideas"]
    for s in shorts:
        md.append(f"- Hook: {s['hook']} | Concept: {s['concept']} | Caption: {s['caption']}")
    md += ["\n## Social Posts"]
    md += [f"### {platform}\n{post}\n" for platform, post in posts.items()]
    md += ["\n## Weekly Organic Plan"]
    md += [f"- {x}" for x in plan]

    return {"seo": seo, "shorts": shorts, "posts": posts, "plan": plan, "markdown": "\n".join(md)}


def save_markdown(data: dict[str, Any], filename: str) -> Path:
    path = OUTPUTS / filename
    path.write_text(data["markdown"], encoding="utf-8")
    return path


def safe_name(value: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in value).strip("_")[:60] or "track"


def main() -> None:
    parser = argparse.ArgumentParser(description="Legal YouTube AI Agent System for BANG IT UP MUSIC")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("setup")
    p.set_defaults(func=setup)

    p = sub.add_parser("channel")
    p.set_defaults(func=channel)

    p = sub.add_parser("videos")
    p.add_argument("--max", type=int, default=10)
    p.set_defaults(func=videos)

    p = sub.add_parser("analytics")
    p.add_argument("--days", type=int, default=28)
    p.set_defaults(func=analytics)

    p = sub.add_parser("campaign")
    p.add_argument("--title", required=True)
    p.add_argument("--genre", default="music")
    p.add_argument("--mood", default="high energy")
    p.add_argument("--audience", default="music listeners, DJs, creators")
    p.set_defaults(func=campaign)

    p = sub.add_parser("report")
    p.add_argument("--days", type=int, default=28)
    p.set_defaults(func=report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
