from pathlib import Path

NO_DESCRIPTION = "No description found"

style_block = """
    <style>
  .conv {
    font-family: Georgia, serif;
    max-width: 600px;
  }
  .conv-title {
    font-size: 20px;
    font-weight: bold;
    border-bottom: 2px solid #333;
    padding-bottom: 6px;
    margin-bottom: 4px;
  }
  .conv-sub {
    font-size: 13px;
    color: #666;
    font-style: italic;
    margin-bottom: 16px;
  }
  .hand-req {
    font-size: 14px;
    color: #555;
    font-style: italic;
    border-left: 3px solid #ccc;
    padding-left: 10px;
    margin-bottom: 16px;
    line-height: 1.6;
  }
  .section-heading {
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
    margin: 16px 0 8px;
  }
  .bid-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin-bottom: 8px;
  }
  .bid-table td {
    padding: 5px 8px;
    border-bottom: 1px solid #eee;
    vertical-align: top;
  }
  .bid-table td:first-child {
    width: 70px;
    font-weight: normal;
    white-space: nowrap;
  }
  .bid-table td:last-child {
    color: #555;
  }
  .bid-note {
    font-size: 12px;
    font-style: italic;
    color: #888;
    padding: 2px 8px 8px 8px;
  }
  .points-grid {
    display: grid;
    grid-template-columns: 120px 1fr;
    font-size: 14px;
  }
  .points-grid div {
    padding: 5px 8px 5px 0;
    border-bottom: 1px solid #eee;
  }
  .points-label { color: #333; }
  .points-action { color: #555; }
  .rebid-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 14px;
  }
  .rebid-list li {
    padding: 6px 0 6px 16px;
    border-bottom: 1px solid #eee;
    color: #555;
    line-height: 1.5;
    position: relative;
  }
  .rebid-list li::before {
    content: "–";
    position: absolute;
    left: 0;
    color: #aaa;
  }
  .rebid-list li b {
    color: #222;
    font-weight: 600;
  }
  .r { color: #c0392b; }
</style>
"""

style_block_large = """
    <style>
  .conv {
    font-family: Georgia, serif;
    max-width: 700px;
  }
  .conv-title {
    font-size: 26px;
    font-weight: bold;
    border-bottom: 2px solid #333;
    padding-bottom: 8px;
    margin-bottom: 6px;
  }
  .conv-sub {
    font-size: 15px;
    color: #666;
    font-style: italic;
    margin-bottom: 20px;
  }
  .hand-req {
    font-size: 16px;
    color: #555;
    font-style: italic;
    border-left: 3px solid #ccc;
    padding-left: 12px;
    margin-bottom: 20px;
    line-height: 1.7;
  }
  .section-heading {
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
    margin: 20px 0 10px;
  }
  .bid-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 16px;
    margin-bottom: 10px;
  }
  .bid-table td {
    padding: 7px 10px;
    border-bottom: 1px solid #eee;
    vertical-align: top;
    text-align: left;
  }
  .bid-table td:first-child {
    width: 80px;
    font-weight: normal;
    white-space: nowrap;
  }
  .bid-table td:last-child {
    color: #555;
    text-align: left;
  }
  .bid-note {
    font-size: 14px;
    font-style: italic;
    color: #888;
    padding: 2px 10px 10px 10px;
    text-align: left;
  }
  .points-grid {
    display: grid;
    grid-template-columns: 140px 1fr;
    font-size: 16px;
  }
  .points-grid div {
    padding: 6px 10px 6px 0;
    border-bottom: 1px solid #eee;
    text-align: left;
  }
  .points-label { color: #333; }
  .points-action { color: #555; }
  .rebid-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 16px;
  }
  .rebid-list li {
    padding: 8px 0 8px 18px;
    border-bottom: 1px solid #eee;
    color: #555;
    line-height: 1.6;
    position: relative;
    text-align: left;
  }
  .rebid-list li::before {
    content: "–";
    position: absolute;
    left: 0;
    color: #aaa;
  }
  .rebid-list li b {
    color: #222;
    font-weight: 600;
  }
  .r { color: #c0392b; }
</style>
"""


def get_description(file: str) -> str:
    loop = 0
    parent = Path(__file__)
    while loop < 10:
        path = Path(parent, "html", file)
        if not path.parent:
            loop = 10
            return NO_DESCRIPTION

        if not Path(parent, "html", file).exists():
            parent = parent.parent
            loop += 1
            continue

        with open(Path(parent, "html", file)) as f_description:
            description = f_description.read()

        return f"{style_block_large}{description}"
    print(f"Could not find description for {file}")
    return NO_DESCRIPTION
