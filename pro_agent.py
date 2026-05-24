from __future__ import annotations

import json
import os
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any

from agents.analytics_agent import AnalyticsAgent
from agents.collaboration_agent import CollaborationAgent
from agents.distribution_agent import DistributionAgent
from agents.llm_agent import LocalLLMAgent
from agents.planner_agent import PlannerAgent
from agents.promotion_agent import PromotionAgent
from agents.seo_agent import SEOAgent, SEOInput
from agents.shorts_agent import ShortsAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.trend_agent import TrendAgent
from youtube_api.client import YouTubeClient

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
DATA = ROOT / "data"
DASH = ROOT / "dashboard"
OUTPUTS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input("\nΠάτα Enter για συνέχεια...")


def safe_name(value: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in value).strip("_")[:70] or "track"


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def md_section(title: str, items: list[str]) -> list[str]:
    return [f"\n## {title}"] + [f"- {x}" for x in items]


def pro_campaign(title: str, genre: str, mood: str, audience: str, url: str = "https://www.youtube.com/@BANGITUPMUSIC") -> dict[str, Any]:
    seo = SEOAgent().generate(SEOInput(title=title, genre=genre, mood=mood, audience=audience))
    shorts = ShortsAgent().generate(title, genre, mood)
    trend = TrendAgent().ideas(genre, mood)
    thumb = ThumbnailAgent().recommend(title)
    dist = DistributionAgent().package(title, url)
    collab = CollaborationAgent().targets_and_message(genre)
    plan = PlannerAgent().seven_day_plan(title)
    context = {"title": title, "genre": genre, "mood": mood, "audience": audience, "seo": seo, "trend": trend, "plan": plan}
    ai_strategy = LocalLLMAgent().strategy_from_context(context)

    lines: list[str] = [
        f"# PRO Campaign: {title}",
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "\n## SEO Titles",
        *[f"- {x}" for x in seo["titles"]],
        "\n## YouTube Description",
        str(seo["description"]),
        "\n## Hashtags",
        " ".join(seo["hashtags"]),
        "\n## Tags",
        ", ".join(seo["tags"]),
        "\n## Pinned Comment",
        str(seo["pinned_comment"]),
        "\n## Shorts Factory",
    ]
    for s in shorts:
        lines.append(f"- Hook: {s['hook']} | Concept: {s['concept']} | Caption: {s['caption']}")
    lines += md_section("Trend Keywords", trend["keywords"])
    lines += md_section("Viral Short Formats", trend["short_formats"])
    lines += md_section("Thumbnail Recommendations", thumb)
    lines += ["\n## Cross-platform Distribution"]
    lines += [f"### {k}\n{v}\n" for k, v in dist.items()]
    lines += ["\n## Collaboration Targets"] + [f"- {x}" for x in collab["targets"]]
    lines += ["\n## Collaboration Message", str(collab["message_template"])]
    lines += md_section("7-Day Action Plan", plan)
    lines += ["\n## Local AI Strategy", ai_strategy]
    lines += ["\n## Compliance", "Δεν χρησιμοποιεί fake views, fake subscribers, bots ή spam. Όλα είναι οργανική προώθηση."]

    data = {"title": title, "genre": genre, "mood": mood, "audience": audience, "seo": seo, "shorts": shorts, "trend": trend, "thumbnail": thumb, "distribution": dist, "collaboration": collab, "plan": plan, "ai_strategy": ai_strategy, "markdown": "\n".join(lines)}
    base = safe_name(title)
    (OUTPUTS / f"pro_campaign_{base}.md").write_text(data["markdown"], encoding="utf-8")
    write_json(DATA / "latest_campaign.json", data)
    update_dashboard(data)
    return data


def full_pro_report() -> Path:
    yt = YouTubeClient()
    ch = yt.my_channel()
    videos = yt.recent_videos(max_results=10)
    analytics = yt.analytics_summary(days=28)
    recs = AnalyticsAgent().recommend_from_summary(analytics)
    top = yt.top_videos_by_views(days=28, max_results=10)
    context = {"channel": ch.get("snippet", {}), "analytics_recommendations": recs, "top_videos": top.get("raw", {})}
    ai = LocalLLMAgent().strategy_from_context(context)

    lines = [
        "# BANG IT UP MUSIC — PRO Growth Report",
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Channel: {ch['snippet'].get('title','')}",
        f"Analytics period: {analytics['start']} → {analytics['end']}",
        "\n## Analytics Recommendations",
        *[f"- {x}" for x in recs],
        "\n## Recent Videos",
    ]
    for v in videos:
        stats = v.get("statistics", {})
        lines.append(f"- {v['snippet'].get('title','')}: {stats.get('viewCount','0')} views, {stats.get('likeCount','0')} likes, {stats.get('commentCount','0')} comments")
    lines += md_section("Next 7 Days", PlannerAgent().seven_day_plan("το καλύτερο πρόσφατο track"))
    lines += md_section("Trend Keywords", TrendAgent().ideas()["keywords"])
    lines += ["\n## Local AI Strategy", ai]
    lines += ["\n## Safe Growth Rules", "Μόνο οργανική προώθηση. Όχι bots, όχι fake engagement, όχι spam."]

    path = OUTPUTS / "pro_growth_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    write_json(DATA / "latest_report.json", {"recommendations": recs, "recent_videos": videos, "analytics": analytics, "ai_strategy": ai})
    update_dashboard()
    return path


def update_dashboard(campaign: dict[str, Any] | None = None) -> None:
    latest_campaign = campaign
    if latest_campaign is None and (DATA / "latest_campaign.json").exists():
        latest_campaign = json.loads((DATA / "latest_campaign.json").read_text(encoding="utf-8"))
    report_text = ""
    for p in [OUTPUTS / "pro_growth_report.md", OUTPUTS / "growth_report.md"]:
        if p.exists():
            report_text = p.read_text(encoding="utf-8")
            break
    html = f"""<!doctype html>
<html lang='el'>
<head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>BANG IT UP MUSIC AI Agents</title>
<style>
body{{margin:0;font-family:Arial, sans-serif;background:#09090f;color:#f5f5f5}} .wrap{{max-width:1100px;margin:auto;padding:24px}}
.card{{background:#151522;border:1px solid #2b2b3d;border-radius:18px;padding:20px;margin:16px 0;box-shadow:0 10px 30px #0006}}
h1{{font-size:34px}} h2{{color:#82f7ff}} pre{{white-space:pre-wrap;background:#05050a;padding:16px;border-radius:12px;overflow:auto}}
.badge{{display:inline-block;background:#30205d;color:#fff;border-radius:999px;padding:6px 10px;margin:4px}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
</style></head><body><div class='wrap'>
<h1>ΒANG IT UP MUSIC — PRO AI Agents</h1>
<p>Νόμιμο οργανικό growth σύστημα. Δεν κάνει bots/fake views/spam.</p>
<div class='grid'>
<div class='card'><h2>Agents</h2><span class='badge'>Growth</span><span class='badge'>Trend</span><span class='badge'>Shorts</span><span class='badge'>Thumbnail</span><span class='badge'>Distribution</span><span class='badge'>Collaboration</span><span class='badge'>Local AI</span></div>
<div class='card'><h2>Next Action</h2><p>Τρέξε το <b>PRO_RUN_WINDOWS.bat</b> και πάτα 2 για νέο campaign ή 3 για full report.</p></div>
</div>
<div class='card'><h2>Latest Campaign</h2><pre>{json.dumps(latest_campaign or {'info':'Δεν υπάρχει ακόμα campaign. Πάτα 2 στο PRO menu.'}, ensure_ascii=False, indent=2)[:12000]}</pre></div>
<div class='card'><h2>Latest Report</h2><pre>{report_text[:12000] or 'Δεν υπάρχει ακόμα report. Πάτα 3 στο PRO menu.'}</pre></div>
</div></body></html>"""
    (DASH / "index.html").write_text(html, encoding="utf-8")


def menu() -> None:
    while True:
        clear()
        print("BANG IT UP MUSIC — PRO AI AGENTS")
        print("=" * 42)
        print("1. Σύνδεση / έλεγχος YouTube OAuth")
        print("2. Φτιάξε PRO campaign για νέο τραγούδι")
        print("3. Φτιάξε PRO growth report από YouTube analytics")
        print("4. Άνοιξε dashboard στο browser")
        print("5. Έλεγχος Ollama / Local AI")
        print("0. Έξοδος")
        choice = input("\nΕπιλογή: ").strip()
        try:
            if choice == "1":
                yt = YouTubeClient(); ch = yt.my_channel(); print(f"\nΣυνδέθηκε: {ch['snippet'].get('title','')}"); pause()
            elif choice == "2":
                title = input("Τίτλος τραγουδιού: ").strip() or "New Track"
                genre = input("Genre: ").strip() or "EDM / Trap / Club"
                mood = input("Mood: ").strip() or "high energy"
                audience = input("Κοινό στόχος: ").strip() or "music listeners, DJs, creators"
                data = pro_campaign(title, genre, mood, audience)
                print("\nΈτοιμο campaign:", OUTPUTS / f"pro_campaign_{safe_name(title)}.md")
                pause()
            elif choice == "3":
                path = full_pro_report(); print("\nΈτοιμο report:", path); pause()
            elif choice == "4":
                update_dashboard(); webbrowser.open((DASH / "index.html").resolve().as_uri()); print("\nΆνοιξε το dashboard."); pause()
            elif choice == "5":
                llm = LocalLLMAgent(); print("\nOllama:", "Βρέθηκε" if llm.available() else "Δεν βρέθηκε - το σύστημα δουλεύει με fallback"); pause()
            elif choice == "0":
                break
        except Exception as exc:
            print("\nΣφάλμα:", exc)
            pause()


if __name__ == "__main__":
    menu()
