#!/usr/bin/env python3
import copy
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W, "r": R}

ET.register_namespace("w", W)
ET.register_namespace("r", R)


def qn(ns, tag):
    return f"{{{ns}}}{tag}"


def w_el(tag, attrs=None, text=None):
    el = ET.Element(qn(W, tag), attrs or {})
    if text is not None:
        el.text = text
    return el


def attr(name):
    return qn(W, name)


def rel_attr(name):
    return qn(R, name)


def para_text(p):
    return "".join(t.text or "" for t in p.iter(qn(W, "t")))


def run(text, bold=False, italic=False, size=26):
    r = w_el("r")
    rpr = w_el("rPr")
    rfonts = w_el("rFonts", {
        attr("ascii"): "Times New Roman",
        attr("hAnsi"): "Times New Roman",
        attr("eastAsia"): "Times New Roman",
        attr("cs"): "Times New Roman",
    })
    rpr.append(rfonts)
    if bold:
        rpr.append(w_el("b"))
        rpr.append(w_el("bCs"))
    if italic:
        rpr.append(w_el("i"))
        rpr.append(w_el("iCs"))
    rpr.append(w_el("sz", {attr("val"): str(size)}))
    rpr.append(w_el("szCs", {attr("val"): str(size)}))
    r.append(rpr)
    t_attrs = {}
    if text.startswith(" ") or text.endswith(" "):
        t_attrs["{http://www.w3.org/XML/1998/namespace}space"] = "preserve"
    t = w_el("t", t_attrs, text)
    r.append(t)
    return r


def add_inline_runs(p, text, bold=False, italic=False, size=26):
    text = text.replace("\\", "")
    parts = text.split("**")
    active_bold = bold
    for i, part in enumerate(parts):
        if part:
            p.append(run(part, bold=active_bold, italic=italic, size=size))
        if i != len(parts) - 1:
            active_bold = not active_bold


def paragraph(text="", *, style=None, bold=False, italic=False, center=False,
              justify=True, page_break=False, list_kind=None, indent=None,
              before=0, after=120, size=26, keep_next=False):
    p = w_el("p")
    ppr = w_el("pPr")
    if style:
        ppr.append(w_el("pStyle", {attr("val"): style}))
    if page_break:
        ppr.append(w_el("pageBreakBefore"))
    if keep_next:
        ppr.append(w_el("keepNext"))
    spacing = w_el("spacing", {
        attr("before"): str(before),
        attr("after"): str(after),
        attr("line"): "360",
        attr("lineRule"): "auto",
    })
    ppr.append(spacing)
    if list_kind == "bullet":
        num_pr = w_el("numPr")
        num_pr.append(w_el("ilvl", {attr("val"): "0"}))
        num_pr.append(w_el("numId", {attr("val"): "9"}))
        ppr.append(num_pr)
    elif list_kind == "number":
        num_pr = w_el("numPr")
        num_pr.append(w_el("ilvl", {attr("val"): "0"}))
        num_pr.append(w_el("numId", {attr("val"): "2"}))
        ppr.append(num_pr)
    if indent is not None:
        ppr.append(w_el("ind", {attr("left"): str(indent)}))
    if center:
        ppr.append(w_el("jc", {attr("val"): "center"}))
    elif justify:
        ppr.append(w_el("jc", {attr("val"): "both"}))
    p.append(ppr)
    if text:
        add_inline_runs(p, text, bold=bold, italic=italic, size=size)
    return p


def table(rows):
    tbl = w_el("tbl")
    tbl_pr = w_el("tblPr")
    tbl_pr.append(w_el("tblW", {attr("w"): "9070", attr("type"): "dxa"}))
    border = {attr("val"): "single", attr("sz"): "4", attr("space"): "0", attr("color"): "666666"}
    borders = w_el("tblBorders")
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        borders.append(w_el(side, border))
    tbl_pr.append(borders)
    tbl.append(tbl_pr)
    widths = [2268] * max(1, len(rows[0]))
    for row in rows:
        tr = w_el("tr")
        for i, cell in enumerate(row):
            tc = w_el("tc")
            tc_pr = w_el("tcPr")
            tc_pr.append(w_el("tcW", {attr("w"): str(widths[min(i, len(widths)-1)]), attr("type"): "dxa"}))
            tc_pr.append(w_el("tcMar"))
            tc.append(tc_pr)
            tc.append(paragraph(cell.strip(), bold="**" in cell, justify=False, after=60, size=24))
            tr.append(tc)
        tbl.append(tr)
    return tbl


def sect_pr():
    sp = w_el("sectPr")
    sp.append(w_el("headerReference", {attr("type"): "default", rel_attr("id"): "rId4"}))
    sp.append(w_el("footerReference", {attr("type"): "default", rel_attr("id"): "rId5"}))
    sp.append(w_el("pgSz", {attr("w"): "11906", attr("h"): "16838"}))
    sp.append(w_el("pgMar", {
        attr("top"): "1134",
        attr("right"): "1134",
        attr("bottom"): "1134",
        attr("left"): "1701",
        attr("header"): "720",
        attr("footer"): "720",
        attr("gutter"): "0",
    }))
    sp.append(w_el("cols", {attr("space"): "720"}))
    sp.append(w_el("docGrid", {attr("linePitch"): "360"}))
    return sp


def header_xml():
    hdr = ET.Element(qn(W, "hdr"))
    p = paragraph("", center=True, justify=False, after=0, size=24)
    p.append(w_el("r"))
    r1 = w_el("r")
    r1.append(w_el("fldChar", {attr("fldCharType"): "begin"}))
    r2 = w_el("r")
    r2.append(w_el("instrText", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"}, " PAGE "))
    r3 = w_el("r")
    r3.append(w_el("fldChar", {attr("fldCharType"): "separate"}))
    r4 = run("1", size=24)
    r5 = w_el("r")
    r5.append(w_el("fldChar", {attr("fldCharType"): "end"}))
    for r in [r1, r2, r3, r4, r5]:
        p.append(r)
    hdr.append(p)
    return ET.tostring(hdr, encoding="utf-8", xml_declaration=True)


def normalize_text(text):
    text = text.strip()
    text = text.replace("Website", "website")
    text = text.replace("tối hóa", "tối ưu hóa")
    return text


def is_chapter(text):
    return text.startswith("CHƯƠNG ") or text in {
        "MỞ ĐẦU",
        "KẾT LUẬN VÀ KIẾN NGHỊ",
        "TÀI LIỆU THAM KHẢO",
        "PHỤ LỤC",
    }


def body_from_source(source_docx, target_docx):
    src_root = ET.fromstring(zipfile.ZipFile(source_docx).read("word/document.xml"))
    tgt_root = ET.fromstring(zipfile.ZipFile(target_docx).read("word/document.xml"))
    src_body = src_root.find("w:body", NS)
    tgt_body = tgt_root.find("w:body", NS)

    new_body = w_el("body")

    # Keep the original template cover page, including logo/image relationship.
    new_body.append(copy.deepcopy(list(tgt_body)[0]))

    # Filled research result summary.
    summary = [
        ("THÔNG TIN KẾT QUẢ NGHIÊN CỨU CỦA ĐỀ TÀI", "title"),
        ("1. Thông tin chung", "h2"),
        ("- Tên đề tài: Ứng dụng chatbot AI tối ưu hóa quy trình xây dựng website", "bullet"),
        ("- Sinh viên/Nhóm sinh viên thực hiện: Vũ Thượng Hải, Lớp ĐH12C1, Khoa Công nghệ thông tin.", "bullet"),
        ("- Người hướng dẫn: TS. Vũ Ngọc Phan", "bullet"),
        ("2. Mục tiêu đề tài", "h2"),
        ("Phát triển quy trình hybrid trong đó con người và chatbot AI (ChatGPT, Claude, Grok) phối hợp để xây dựng website hiệu quả, cá nhân hóa và có khả năng mở rộng; đồng thời đo lường mức giảm thời gian, chi phí và cải thiện chất lượng sản phẩm.", "normal"),
        ("3. Tính mới và sáng tạo", "h2"),
        ("Đề tài so sánh đồng thời ba chatbot AI trong toàn bộ vòng đời xây dựng website gồm discovery, planning, design, content, development, testing và maintenance; từ đó đề xuất chiến lược phối hợp nhiều AI thay vì phụ thuộc vào một công cụ riêng lẻ.", "normal"),
        ("4. Kết quả nghiên cứu", "h2"),
        ("Kết quả chính của đề tài là bộ Website Lifecycle Templates gồm 7 giai đoạn với 33 templates, 17 prompts, 20 patterns, 22 examples; và bộ skill architect-planner-builder giúp thiết kế, lập kế hoạch, triển khai workflow AI có trace, guardrails và kiểm chứng. Các chỉ số năng suất được trình bày theo nguồn nghiên cứu đã công bố hoặc ở mức mục tiêu/pilot, không kết luận phần trăm khi thiếu log dữ liệu thô.", "normal"),
        ("5. Đóng góp về mặt kinh tế - xã hội, giáo dục và đào tạo và khả năng áp dụng của đề tài", "h2"),
        ("Nghiên cứu cung cấp framework, khuyến nghị lựa chọn công cụ, quy trình kiểm soát chất lượng và định hướng đào tạo kỹ năng AI-assisted development cho sinh viên, lập trình viên và doanh nghiệp nhỏ trong quá trình chuyển đổi số.", "normal"),
        ("6. Công bố khoa học của sinh viên từ kết quả nghiên cứu của đề tài hoặc nhận xét, đánh giá của cơ sở đã áp dụng các kết quả nghiên cứu (nếu có)", "h2"),
        ("Chưa có công bố khoa học tại thời điểm hoàn thiện báo cáo.", "normal"),
    ]
    new_body.append(paragraph("", page_break=True, after=0))
    for text, kind in summary:
        if kind == "title":
            new_body.append(paragraph(text, bold=True, center=True, justify=False, before=120, after=180, size=28))
        elif kind == "h2":
            new_body.append(paragraph(text, bold=True, justify=False, before=120, after=80, size=26))
        elif kind == "bullet":
            new_body.append(paragraph(text[2:], list_kind="bullet", indent=720, after=80, size=26))
        else:
            new_body.append(paragraph(text, after=120, size=26))

    new_body.append(paragraph("Hà Nội, ngày ...... tháng ...... năm 2026", italic=True, center=True, justify=False, before=360, after=80))
    new_body.append(paragraph("Sinh viên chịu trách nhiệm chính", bold=True, center=True, justify=False, after=360))
    new_body.append(paragraph("Vũ Thượng Hải", bold=True, center=True, justify=False, after=240))
    new_body.append(paragraph("Nhận xét của người hướng dẫn về những đóng góp khoa học của sinh viên thực hiện đề tài:", italic=True, before=240, after=120))
    new_body.append(paragraph("................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................", italic=True, after=240))
    new_body.append(paragraph("Hà Nội, ngày ...... tháng ...... năm 2026", italic=True, center=True, justify=False, before=240, after=80))
    new_body.append(paragraph("Người hướng dẫn", bold=True, center=True, justify=False, after=360))
    new_body.append(paragraph("TS. Vũ Ngọc Phan", bold=True, center=True, justify=False, after=240))

    toc_items = [
        "MỞ ĐẦU",
        "CHƯƠNG 1. TỔNG QUAN CÁC VẤN ĐỀ NGHIÊN CỨU",
        "CHƯƠNG 2. MỤC TIÊU, ĐỐI TƯỢNG, PHẠM VI, NỘI DUNG NGHIÊN CỨU VÀ PHƯƠNG PHÁP NGHIÊN CỨU",
        "CHƯƠNG 3. KẾT QUẢ VÀ THẢO LUẬN",
        "KẾT LUẬN VÀ KIẾN NGHỊ",
        "TÀI LIỆU THAM KHẢO",
        "PHỤ LỤC",
    ]
    new_body.append(paragraph("MỤC LỤC", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    for item in toc_items:
        new_body.append(paragraph(item, after=80, size=26, justify=False))
    new_body.append(paragraph("DANH MỤC CÁC CHỮ VIẾT TẮT", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    abbrev_rows = [
        ["Từ viết tắt", "Nghĩa đầy đủ"],
        ["AI", "Artificial Intelligence - Trí tuệ nhân tạo"],
        ["LLM", "Large Language Model - Mô hình ngôn ngữ lớn"],
        ["API", "Application Programming Interface"],
        ["SEO", "Search Engine Optimization - Tối ưu hóa công cụ tìm kiếm"],
        ["UI/UX", "User Interface/User Experience"],
    ]
    new_body.append(table(abbrev_rows))

    add_corrected_report_body(new_body)

    new_body.append(paragraph("TÀI LIỆU THAM KHẢO", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    refs = [
        "Barke, S., James, M. B., & Polikarpova, N. (2023), Grounded Copilot: How Programmers Interact with Code-Generating Models, Proceedings of the ACM on Programming Languages. URL: https://arxiv.org/abs/2206.15000",
        "Chen, M. et al. (2021), Evaluating Large Language Models Trained on Code. arXiv:2107.03374. URL: https://arxiv.org/abs/2107.03374",
        "Imperva/Thales (2025), 2025 Imperva Bad Bot Report. URL: https://cpl.thalesgroup.com/about-us/newsroom/2025-imperva-bad-bot-report-ai-internet-traffic",
        "Peng, S., Kalliamvakou, E., Cihon, P., & Demirer, M. (2023), The Impact of AI on Developer Productivity: Evidence from GitHub Copilot. arXiv:2302.06590. URL: https://arxiv.org/abs/2302.06590",
        "Vaithilingam, P., Zhang, T., & Glassman, E. L. (2022), Expectation vs. Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models, CHI 2022. DOI: 10.1145/3491101.3519665.",
        "Anthropic (2025), Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet. URL: https://www.anthropic.com/engineering/swe-bench-sonnet/",
        "Tạp chí Kinh tế và Dự báo (2024), Ứng dụng ChatGPT trong hoạt động học tập của sinh viên trên địa bàn TP. Hà Nội. URL: https://kinhtevadubao.vn/ung-dung-chatgpt-trong-hoat-dong-hoc-tap-cua-sinh-vien-tren-dia-ban-tp-ha-noi-30126.html",
        "AWS/Strand Partners (2025), Khai phá tiềm năng AI của Việt Nam; thông tin công bố lại trên các báo kinh tế trong nước về gần 170.000 doanh nghiệp Việt Nam đã ứng dụng AI.",
        "NIST (2023), Artificial Intelligence Risk Management Framework (AI RMF 1.0). URL: https://www.nist.gov/itl/ai-risk-management-framework",
        "OWASP (2025), OWASP Top 10 for Large Language Model Applications. URL: https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "W3C (2023), Web Content Accessibility Guidelines (WCAG) 2.2. URL: https://www.w3.org/TR/WCAG22/",
        "Google Search Central (2023), Google Search's guidance about AI-generated content. URL: https://developers.google.com/search/blog/2023/02/google-search-and-ai-content",
        "Google web.dev (2024), Core Web Vitals documentation. URL: https://web.dev/articles/vitals",
        "MDN Web Docs (2024), Progressive web apps. URL: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps",
        "Website Lifecycle Templates (2026), Bộ tài liệu nội bộ của đề tài tại website-lifecycle-templates/, verified 2026-04-23.",
        "Skill Suite (2026), Bộ skill nội bộ skill-architect, skill-planner, skill-builder do nhóm đề tài thiết kế và thử nghiệm.",
    ]
    for i, ref in enumerate(refs, 1):
        new_body.append(paragraph(f"{i}. {ref}", after=80, size=26))

    new_body.append(paragraph("PHỤ LỤC", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    new_body.append(paragraph("Phụ lục 1. Bộ tiêu chí đánh giá hiệu quả chatbot AI trong quy trình xây dựng website.", bold=True, justify=False, after=120))
    appendix_rows = [
        ["Tiêu chí", "Cách đo lường"],
        ["Thời gian phát triển", "Tổng số giờ thực hiện theo từng giai đoạn; cần log thời gian nếu muốn kết luận định lượng"],
        ["Chi phí", "Chi phí nhân công, API và công cụ hỗ trợ; không kết luận phần trăm nếu thiếu dữ liệu thô"],
        ["Chất lượng code", "Code review, test coverage, bug report, lint/static analysis"],
        ["Hiệu năng", "Lighthouse score, thời gian tải trang, Core Web Vitals"],
        ["Bảo mật", "Số lỗi bảo mật phát hiện qua review, SAST/DAST và kiểm thử thủ công"],
        ["Chất lượng workflow AI", "Mức đầy đủ của input, trace, log, checklist, số lần phải sửa do hallucination"],
    ]
    new_body.append(table(appendix_rows))
    new_body.append(sect_pr())
    tgt_root.remove(tgt_body)
    tgt_root.append(new_body)
    return ET.tostring(tgt_root, encoding="utf-8", xml_declaration=True)

    src_paras = [normalize_text(para_text(p)) for p in src_body.findall("w:p", NS)]
    start = next(i for i, t in enumerate(src_paras) if t == "MỞ ĐẦU")
    table_buffer = []
    for text in src_paras[start:]:
        if not text:
            continue
        if re.fullmatch(r"\|[-:\\s|]+\|", text):
            continue
        if text.startswith("|") and text.endswith("|"):
            cells = [c.strip().replace("**", "") for c in text.strip("|").split("|")]
            table_buffer.append(cells)
            continue
        if table_buffer:
            new_body.append(table(table_buffer))
            table_buffer = []

        if text == "KẾT LUẬN VÀ KIẾN NGHỊ":
            add_research_products(new_body)

        page = is_chapter(text)
        if page:
            new_body.append(paragraph(text, bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28, keep_next=True))
        elif re.match(r"^\d+(\.\d+)+\.", text) or re.match(r"^\d+\.\s", text):
            new_body.append(paragraph(text, bold=True, justify=False, before=120, after=120, size=26, keep_next=True))
        elif text.startswith("- "):
            new_body.append(paragraph(text[2:], list_kind="bullet", indent=720, after=80, size=26))
        else:
            new_body.append(paragraph(text, after=120, size=26))
    if table_buffer:
        new_body.append(table(table_buffer))

    new_body.append(paragraph("TÀI LIỆU THAM KHẢO", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    refs = [
        "Barke, S., James, M. B., & Polikarpova, N. (2023), Grounded Copilot: How Programmers Interact with Code-Generating Models.",
        "Chen, M. et al. (2021), Evaluating Large Language Models Trained on Code, OpenAI.",
        "Peng, S. et al. (2023), The Impact of AI on Developer Productivity: Evidence from GitHub Copilot.",
        "Vaithilingam, P., Zhang, T., & Glassman, E. L. (2022), Expectation vs. Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models.",
        "VINASA (2025), Báo cáo chuyển đổi số và ứng dụng AI trong doanh nghiệp công nghệ Việt Nam.",
        "OpenAI (2024-2025), ChatGPT and API documentation.",
        "Anthropic (2024-2025), Claude documentation and model reports.",
        "xAI (2024-2025), Grok product information and technical updates.",
    ]
    for i, ref in enumerate(refs, 1):
        new_body.append(paragraph(f"{i}. {ref}", after=80, size=26))

    new_body.append(paragraph("PHỤ LỤC", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    new_body.append(paragraph("Phụ lục 1. Bộ tiêu chí đánh giá hiệu quả chatbot AI trong quy trình xây dựng website.", bold=True, justify=False, after=120))
    appendix_rows = [
        ["Tiêu chí", "Cách đo lường"],
        ["Thời gian phát triển", "Tổng số giờ thực hiện theo từng giai đoạn"],
        ["Chi phí", "Chi phí nhân công, API và công cụ hỗ trợ"],
        ["Chất lượng code", "Code coverage, bug density, lint/static analysis"],
        ["Hiệu năng", "Lighthouse score, thời gian tải trang"],
        ["Bảo mật", "Số lỗi bảo mật phát hiện qua review và công cụ quét"],
    ]
    new_body.append(table(appendix_rows))
    new_body.append(sect_pr())
    tgt_root.remove(tgt_body)
    tgt_root.append(new_body)
    return ET.tostring(tgt_root, encoding="utf-8", xml_declaration=True)


def add_corrected_report_body(new_body):
    new_body.append(paragraph("MỞ ĐẦU", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    intro = [
        "Trong những năm gần đây, các mô hình ngôn ngữ lớn và chatbot AI đã trở thành công cụ hỗ trợ quan trọng trong phát triển phần mềm. Đối với quy trình xây dựng website, AI có thể hỗ trợ nhiều hoạt động như phân tích yêu cầu, lập kế hoạch, tạo nội dung, sinh mã nguồn, kiểm thử, rà soát bảo mật và bảo trì. Tuy nhiên, hiệu quả thực tế phụ thuộc mạnh vào cách tổ chức workflow, chất lượng dữ liệu đầu vào, năng lực kiểm tra của con người và cơ chế kiểm soát đầu ra.",
        "Báo cáo này điều chỉnh cách tiếp cận theo hướng thận trọng về số liệu. Thay vì khẳng định rằng AI chiếm 58,8% lưu lượng web toàn cầu, báo cáo sử dụng nguồn Imperva/Thales 2025: traffic tự động, bao gồm bot và các bot chịu tác động từ AI/LLM, chiếm 51% lưu lượng web năm 2024. Con số này cho thấy môi trường web đang chịu tác động mạnh từ tự động hóa, nhưng không đồng nghĩa toàn bộ lượng truy cập đó là traffic từ chatbot AI.",
        "Về năng suất lập trình, báo cáo không xem các con số nội bộ như giảm 36,3% thời gian hay 35% chi phí là kết luận thực nghiệm vì chưa có log thời gian, repo kiểm chứng hoặc dashboard đo lường. Thay vào đó, báo cáo dựa vào các nghiên cứu đã công bố, nổi bật là Peng et al. (2023), trong đó nhóm sử dụng GitHub Copilot hoàn thành một tác vụ lập trình nhanh hơn 55,8% so với nhóm đối chứng. Đồng thời, Vaithilingam et al. (2022) cho thấy AI code assistant không luôn cải thiện thời gian hoặc tỷ lệ hoàn thành, và người dùng vẫn gặp khó khăn khi hiểu, chỉnh sửa, gỡ lỗi code do AI đề xuất.",
        "Từ bối cảnh đó, đề tài không chỉ nghiên cứu việc dùng chatbot AI để tạo code, mà tập trung vào việc xây dựng một mô hình cộng tác người - AI có kiểm soát cho toàn bộ vòng đời website. Hai sản phẩm chính của đề tài là bộ tài liệu Website Lifecycle Templates và bộ skill architect-planner-builder, nhằm chuẩn hóa đầu vào, quy trình và đầu ra khi dùng AI trong phát triển website.",
    ]
    for p in intro:
        new_body.append(paragraph(p, after=120, size=26))

    new_body.append(paragraph("CHƯƠNG 1. TỔNG QUAN CÁC VẤN ĐỀ NGHIÊN CỨU", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    new_body.append(paragraph("1.1. Tổng quan các công trình nghiên cứu trong nước", bold=True, justify=False, before=120, after=120, size=26))
    domestic = [
        "Ở Việt Nam, các nghiên cứu về ChatGPT và AI trong giáo dục cho thấy mức độ tiếp cận của sinh viên với chatbot AI khá cao. Một nghiên cứu đăng trên Tạp chí Kinh tế và Dự báo năm 2024 khảo sát 401 sinh viên tại Hà Nội, ghi nhận 97,01% sinh viên biết đến Chatbot và 78,92% sử dụng ChatGPT trong học tập. Kết quả này cho thấy chatbot AI đã trở thành công cụ quen thuộc trong môi trường học tập, tạo tiền đề để sinh viên ngành công nghệ thông tin sử dụng AI cho các hoạt động lập trình và xây dựng sản phẩm số.",
        "Tuy vậy, phần lớn nghiên cứu trong nước hiện tập trung vào mức độ chấp nhận, hành vi sử dụng hoặc tác động trong học tập. Các nghiên cứu chuyên sâu về việc dùng chatbot AI để chuẩn hóa toàn bộ quy trình xây dựng website, từ discovery đến maintenance, vẫn còn hạn chế. Đây là khoảng trống mà đề tài hướng tới.",
        "Ở phía doanh nghiệp, các công bố gần đây về nghiên cứu của AWS/Strand Partners cho biết khoảng 18% doanh nghiệp Việt Nam đã triển khai AI, tương đương gần 170.000 doanh nghiệp, tăng so với năm trước. Tuy nhiên, phần lớn mới dùng AI ở mức tối ưu vận hành hoặc tinh giản quy trình. Điều này cho thấy nhu cầu về các framework ứng dụng AI có cấu trúc, dễ triển khai và dễ kiểm soát vẫn còn lớn.",
    ]
    for p in domestic:
        new_body.append(paragraph(p, after=120, size=26))

    new_body.append(paragraph("1.2. Tổng quan các công trình nghiên cứu ngoài nước", bold=True, justify=False, before=120, after=120, size=26))
    intl = [
        "Chen et al. (2021) giới thiệu Codex, mô hình GPT được fine-tune trên code công khai từ GitHub. Trên bộ HumanEval, Codex đạt pass@1 = 28,8%, trong khi GPT-3 gần như không giải được bài nào. Kết quả này đánh dấu bước tiến quan trọng của mô hình ngôn ngữ lớn trong sinh mã nguồn, đồng thời cũng cho thấy các mô hình vẫn có giới hạn và cần cơ chế kiểm tra bằng test.",
        "Peng et al. (2023) thực hiện thí nghiệm có kiểm soát với GitHub Copilot và ghi nhận nhóm sử dụng AI hoàn thành tác vụ nhanh hơn 55,8% so với nhóm không dùng AI. Đây là bằng chứng thực nghiệm mạnh về tiềm năng tăng năng suất trong một loại tác vụ cụ thể. Tuy nhiên, kết quả không nên được suy rộng tùy tiện cho mọi dự án website hoặc mọi giai đoạn phát triển.",
        "Vaithilingam et al. (2022) nghiên cứu 24 lập trình viên sử dụng Copilot và chỉ ra rằng Copilot không nhất thiết cải thiện thời gian hoàn thành hoặc tỷ lệ thành công, nhưng nhiều người vẫn muốn dùng vì công cụ cung cấp điểm khởi đầu và giảm công tìm kiếm. Nghiên cứu cũng nhấn mạnh khó khăn trong việc hiểu, chỉnh sửa và gỡ lỗi code do AI tạo ra.",
        "Barke et al. (2023) cho thấy lập trình viên tương tác với Copilot theo hai chế độ chính: acceleration mode, khi họ đã biết cần làm gì và dùng AI để đi nhanh hơn; và exploration mode, khi họ chưa chắc hướng giải quyết và dùng AI để khám phá lựa chọn. Kết luận này phù hợp với định hướng của đề tài: AI nên được đặt trong workflow có vai trò rõ ràng, không thay thế hoàn toàn lập trình viên.",
        "Các benchmark của Anthropic về Claude 3.5 Sonnet trên SWE-bench Verified cho thấy mô hình có năng lực đáng kể trong các tác vụ kỹ thuật phần mềm thực tế. Tuy nhiên, báo cáo này không sử dụng các claim thiếu nguồn như 'Claude gấp 3 lần DeepSeek'; thay vào đó chỉ ghi nhận rằng Claude là một trong các mô hình mạnh cho reasoning và coding theo các benchmark công bố.",
    ]
    for p in intl:
        new_body.append(paragraph(p, after=120, size=26))

    new_body.append(paragraph("1.3. Hạn chế của các nghiên cứu hiện có và lý do cần nghiên cứu", bold=True, justify=False, before=120, after=120, size=26))
    gap_rows = [
        ["Nhóm vấn đề", "Hạn chế trong tài liệu hiện có", "Hướng xử lý của đề tài"],
        ["Phạm vi", "Nhiều nghiên cứu tập trung vào coding hoặc một công cụ AI riêng lẻ", "Mở rộng sang toàn bộ lifecycle website"],
        ["Phương pháp", "Thiếu framework chuyển chatbot từ trả lời tự do sang workflow có kiểm soát", "Thiết kế bộ skill có input/output, gate, trace và validation"],
        ["Dữ liệu", "Dễ lạm dụng số liệu năng suất nếu thiếu log và kiểm định", "Tách rõ benchmark bên ngoài, pilot nội bộ và mục tiêu kỳ vọng"],
        ["Ứng dụng", "Nhiều hướng dẫn còn rời rạc, khó tái sử dụng", "Tạo bộ template, prompt, pattern và example theo 7 phase"],
    ]
    new_body.append(table(gap_rows))
    new_body.append(paragraph("Vì vậy, đề tài có ý nghĩa ở hai lớp: lớp khái niệm, thông qua framework cộng tác người - AI cho vòng đời website; và lớp sản phẩm, thông qua bộ template và bộ skill có thể áp dụng trực tiếp trong các dự án website nhỏ hoặc trong môi trường học tập.", after=120, size=26))

    new_body.append(paragraph("CHƯƠNG 2. MỤC TIÊU, ĐỐI TƯỢNG, PHẠM VI, NỘI DUNG NGHIÊN CỨU VÀ PHƯƠNG PHÁP NGHIÊN CỨU", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    ch2 = [
        ("2.1. Mục tiêu nghiên cứu", "Mục tiêu tổng quát là đề xuất và xây dựng một mô hình hỗ trợ phát triển website bằng chatbot AI theo hướng có cấu trúc, có kiểm soát và có thể tái sử dụng. Mục tiêu cụ thể gồm: xây dựng bộ template cho 7 giai đoạn website lifecycle; thiết kế bộ skill architect-planner-builder để tạo workflow AI chuyên biệt; đề xuất cơ chế đánh giá dựa trên thời gian, chất lượng, bảo mật, khả năng trace và mức độ tái sử dụng."),
        ("2.2. Đối tượng và phạm vi nghiên cứu", "Đối tượng nghiên cứu gồm chatbot AI hỗ trợ lập trình và phát triển website, quy trình xây dựng website, bộ tài liệu lifecycle templates và bộ skill agent hóa workflow. Phạm vi tập trung vào website và web application; không đi sâu vào huấn luyện mô hình AI, mobile native hoặc hạ tầng DevOps quy mô lớn."),
        ("2.3. Nội dung nghiên cứu", "Nội dung gồm tổng quan tài liệu; phân tích vai trò AI trong từng phase website lifecycle; xây dựng bộ template/prompt/pattern/example; thiết kế pipeline skill-architect, skill-planner, skill-builder; và đề xuất phương pháp đánh giá kết quả. Các case như website bán hoa hoặc corporate website chỉ được dùng như ví dụ minh họa/pilot, không trình bày như thực nghiệm có kiểm định nếu thiếu dữ liệu thô."),
        ("2.4. Phương pháp nghiên cứu", "Đề tài sử dụng phương pháp tổng quan tài liệu, phân tích thiết kế hệ thống, xây dựng artefact, thử nghiệm thí điểm và đánh giá định tính. Khi chưa có log thời gian, repo, test report hoặc dữ liệu đo lường đầy đủ, báo cáo chỉ trình bày kết quả ở mức pilot/khái niệm, không kết luận phần trăm giảm thời gian hoặc chi phí."),
    ]
    for title, text in ch2:
        new_body.append(paragraph(title, bold=True, justify=False, before=120, after=80, size=26))
        new_body.append(paragraph(text, after=120, size=26))

    new_body.append(paragraph("CHƯƠNG 3. KẾT QUẢ VÀ THẢO LUẬN", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    new_body.append(paragraph("3.1. Kết quả phân tích vai trò của chatbot AI trong website lifecycle", bold=True, justify=False, before=120, after=120, size=26))
    phase_rows = [
        ["Giai đoạn", "Vai trò phù hợp của chatbot AI", "Vai trò bắt buộc của con người"],
        ["Discovery", "Gợi ý câu hỏi yêu cầu, persona, use case, rủi ro", "Xác nhận nhu cầu thật và phạm vi dự án"],
        ["Planning", "Đề xuất sitemap, ADR, milestone, tech stack", "Ra quyết định kiến trúc và ưu tiên nghiệp vụ"],
        ["Design", "Tạo checklist UI/UX, responsive, accessibility", "Đảm bảo bản sắc thương hiệu và trải nghiệm người dùng"],
        ["Content", "Soạn nháp nội dung, metadata, SEO checklist", "Kiểm duyệt tính đúng, giọng văn và pháp lý"],
        ["Development", "Sinh boilerplate, gợi ý API, test mẫu", "Review code, bảo mật, hiệu năng, maintainability"],
        ["Testing", "Sinh test case, checklist, bug report template", "Kiểm thử trải nghiệm thật và edge cases"],
        ["Maintenance", "Gợi ý incident report, changelog, performance report", "Theo dõi production và chịu trách nhiệm vận hành"],
    ]
    new_body.append(table(phase_rows))

    new_body.append(paragraph("3.2. Kết quả xây dựng bộ tài liệu Website Lifecycle Templates", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    new_body.append(paragraph("Bộ Website Lifecycle Templates được tổ chức theo 7 giai đoạn: Discovery, Planning, Design, Content, Development, Testing và Maintenance. Mỗi giai đoạn có bốn nhóm artefact: templates, prompts, patterns và examples. Inventory đã verify gồm 33 templates, 17 prompts, 20 patterns và 22 examples.", after=120, size=26))
    lifecycle_rows = [
        ["Giai đoạn", "Tài liệu tiêu biểu", "Ý nghĩa tối ưu hóa"],
        ["Discovery", "requirements, user stories, use cases, risk analysis", "Chuẩn hóa đầu vào cho AI và nhóm phát triển"],
        ["Planning", "sitemap, ADR, roadmap, tech stack decision", "Giảm mơ hồ khi chọn kiến trúc và phạm vi"],
        ["Design", "design system, component spec, accessibility", "Tăng tính nhất quán UI/UX"],
        ["Content", "SEO checklist, metadata, copywriting brief", "Tăng chất lượng nội dung và khả năng tìm kiếm"],
        ["Development", "API design, database schema, coding standards", "Chuẩn hóa triển khai kỹ thuật"],
        ["Testing", "test plan, security, performance checklist", "Tăng khả năng kiểm chứng chất lượng"],
        ["Maintenance", "incident report, maintenance log, performance baseline", "Hỗ trợ vận hành và cải tiến sau triển khai"],
    ]
    new_body.append(table(lifecycle_rows))

    new_body.append(paragraph("3.3. Kết quả xây dựng bộ skill thiết kế và triển khai workflow AI", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    new_body.append(paragraph("Bộ skill gồm skill-architect, skill-planner và skill-builder được thiết kế để biến chatbot AI thành các agent có vai trò rõ ràng. Mỗi skill có hợp đồng đầu vào/đầu ra, guardrails, progressive disclosure và cơ chế kiểm chứng. Đây là đóng góp sản phẩm quan trọng của đề tài vì nó giải quyết vấn đề phổ biến khi dùng chatbot: phản hồi không ổn định, thiếu trace và khó tái sử dụng.", after=120, size=26))
    skill_rows = [
        ["Thành phần", "Chức năng", "Cơ chế kiểm soát", "Kết quả"],
        ["skill-architect", "Phân tích yêu cầu và thiết kế kiến trúc skill", "Gate xác nhận, 3 Pillars, 7 Zones, Mermaid diagrams", "design.md"],
        ["skill-planner", "Chuyển thiết kế thành kế hoạch triển khai", "Trace tag, audit tài nguyên, dependency detection", "todo.md"],
        ["skill-builder", "Triển khai skill theo thiết kế và kế hoạch", "Zone Contract, build-log, placeholder scale, validation", "Skill hoàn chỉnh"],
    ]
    new_body.append(table(skill_rows))

    new_body.append(paragraph("3.4. Mô hình tích hợp hai sản phẩm vào quy trình xây dựng website", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    new_body.append(paragraph("Website Lifecycle Templates đóng vai trò lớp tri thức và artefact; bộ skill architect-planner-builder đóng vai trò lớp điều phối workflow. Khi kết hợp, chatbot AI có thể nhận yêu cầu, chọn đúng template/prompt/pattern, tạo đầu ra có cấu trúc, sau đó kiểm tra bằng checklist và log. Cách tiếp cận này giúp chuyển AI từ công cụ hỏi đáp sang cộng sự có quy trình.", after=120, size=26))
    integration_rows = [
        ["Lớp", "Vai trò", "Tác động"],
        ["Templates", "Cung cấp biểu mẫu đầu ra chuẩn", "Giảm thời gian soạn tài liệu ban đầu"],
        ["Prompts", "Hướng dẫn AI tạo bản nháp theo phase", "Giảm prompt mơ hồ"],
        ["Patterns", "Cung cấp best practices và workflow", "Tăng chất lượng quyết định"],
        ["Examples", "Minh họa cách điền hoặc áp dụng", "Giảm sai lệch khi sử dụng"],
        ["Skill Suite", "Thiết kế, lập kế hoạch, triển khai workflow AI", "Tăng khả năng tái sử dụng và kiểm chứng"],
    ]
    new_body.append(table(integration_rows))

    new_body.append(paragraph("3.5. Điều chỉnh các claim và giới hạn kết quả", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    correction_rows = [
        ["Claim cũ/sai lệch", "Cách chỉnh trong báo cáo"],
        ["AI chiếm 58,8% lưu lượng web", "Thay bằng traffic tự động chiếm 51% web traffic năm 2024 theo Imperva/Thales; không gọi toàn bộ là traffic chatbot AI"],
        ["Giảm 36,3% thời gian, 35% chi phí", "Chuyển thành mục tiêu/giả định hoặc pilot; không kết luận nếu thiếu log dữ liệu"],
        ["Codex đạt 37% HumanEval", "Sửa thành Codex pass@1 = 28,8% theo Chen et al. (2021)"],
        ["Peng khảo sát 2.000 developer và có số 35%/12%", "Sửa thành thí nghiệm có kiểm soát, kết quả nhóm dùng Copilot nhanh hơn 55,8%"],
        ["Claude gấp 3 lần DeepSeek", "Bỏ claim; chỉ ghi nhận benchmark chính thức của Claude trên coding/reasoning"],
        ["Grok tăng SEO 10-23 lần", "Bỏ claim; chỉ mô tả Grok phù hợp với dữ liệu thời gian thực/X data nếu có nguồn"],
        ["Case flower shop/corporate là thực nghiệm", "Chuyển thành ví dụ minh họa/pilot nếu không có repo, dashboard hoặc test report"],
    ]
    new_body.append(table(correction_rows))

    new_body.append(paragraph("3.6. Thảo luận", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    discussion = [
        "Kết quả của đề tài cho thấy giá trị chính của chatbot AI trong xây dựng website không nằm ở việc thay thế lập trình viên, mà ở khả năng tăng tốc các tác vụ có cấu trúc khi có template, prompt, checklist và dữ liệu đầu vào rõ ràng. Điều này phù hợp với nghiên cứu của Barke et al. về acceleration mode và exploration mode.",
        "Đồng thời, các rủi ro về chất lượng code, bảo mật, hallucination và phụ thuộc nhà cung cấp vẫn tồn tại. Do đó, mọi đầu ra AI cần được kiểm tra bởi con người, chạy test, review bảo mật và lưu lại evidence. Bộ skill suite của đề tài giải quyết vấn đề này bằng cơ chế trace, build-log, gate và validation.",
        "Về tính khả thi, đề tài nên được xem là nghiên cứu thiết kế artefact và pilot nội bộ. Để nâng cấp thành nghiên cứu thực nghiệm đầy đủ, cần bổ sung log thời gian, benchmark task, repo mã nguồn, test report, Lighthouse report và khảo sát người dùng trước/sau khi áp dụng workflow.",
    ]
    for p in discussion:
        new_body.append(paragraph(p, after=120, size=26))

    add_expanded_knowledge_sections(new_body)

    new_body.append(paragraph("KẾT LUẬN VÀ KIẾN NGHỊ", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    new_body.append(paragraph("Kết luận", bold=True, justify=False, before=120, after=120, size=26))
    conclusions = [
        "Đề tài đã xây dựng được một khung ứng dụng chatbot AI trong tối ưu hóa quá trình xây dựng website theo hướng có cấu trúc và có kiểm soát. Hai sản phẩm chính là Website Lifecycle Templates và bộ skill architect-planner-builder.",
        "Bộ Website Lifecycle Templates chuẩn hóa vòng đời website thành 7 giai đoạn với 33 templates, 17 prompts, 20 patterns và 22 examples. Bộ skill suite chuyển quá trình tạo workflow AI thành pipeline gồm thiết kế, lập kế hoạch và triển khai có kiểm chứng.",
        "Báo cáo đã điều chỉnh các claim thiếu nguồn và không còn trình bày các con số nội bộ như kết quả thực nghiệm chắc chắn. Các số liệu về năng suất, bot traffic và benchmark AI được thay bằng nguồn thật và được diễn giải thận trọng.",
    ]
    for p in conclusions:
        new_body.append(paragraph(p, after=120, size=26))
    new_body.append(paragraph("Kiến nghị", bold=True, justify=False, before=120, after=120, size=26))
    recommendations = [
        "Tiếp tục thu thập dữ liệu thực nghiệm: log thời gian, chi phí, số lỗi, test coverage, Lighthouse score và phản hồi người dùng để đánh giá định lượng.",
        "Áp dụng bộ template và skill suite vào một số dự án website pilot có phạm vi nhỏ, sau đó so sánh với quy trình không dùng AI.",
        "Bổ sung tài liệu về bảo mật dữ liệu, kiểm soát bản quyền nội dung AI, kiểm thử accessibility và monitoring/alerting sau triển khai.",
        "Trong đào tạo, nên dạy sinh viên cách dùng AI theo workflow có kiểm chứng thay vì chỉ học cách viết prompt đơn lẻ.",
    ]
    for rec in recommendations:
        new_body.append(paragraph(rec, list_kind="bullet", indent=720, after=80, size=26))


def add_expanded_knowledge_sections(new_body):
    new_body.append(paragraph("CHƯƠNG 4. CƠ SỞ TRIỂN KHAI AI CHATBOT TRONG TỐI ƯU PHÁT TRIỂN WEBSITE", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    sections = [
        (
            "4.1. Vai trò của AI chatbot trong mô hình cộng tác người - máy",
            [
                "AI chatbot trong phát triển website nên được hiểu là một công cụ cộng tác tri thức chứ không phải một hệ thống tự động hóa hoàn toàn. Trong các giai đoạn đầu như discovery và planning, chatbot giúp mở rộng không gian câu hỏi, gợi ý persona, phát hiện rủi ro và tạo bản nháp tài liệu. Ở giai đoạn development, chatbot có thể sinh boilerplate, giải thích API, đề xuất test case và hỗ trợ gỡ lỗi. Tuy nhiên, quyền quyết định cuối cùng vẫn thuộc về con người vì website luôn gắn với mục tiêu kinh doanh, trải nghiệm người dùng, trách nhiệm bảo mật và ràng buộc pháp lý.",
                "Kết quả từ các nghiên cứu về Copilot cho thấy AI có thể làm tăng tốc độ hoàn thành một số tác vụ cụ thể, nhưng hiệu quả này không đồng đều. Peng et al. (2023) cho thấy tác vụ lập trình nhỏ có thể hoàn thành nhanh hơn khi dùng Copilot, trong khi Vaithilingam et al. (2022) nhấn mạnh rằng người dùng vẫn phải hiểu, chỉnh sửa và gỡ lỗi code AI tạo ra. Điều đó dẫn đến một nguyên tắc quan trọng: AI không thay thế quy trình kỹ thuật phần mềm, mà cần được đặt vào quy trình với kiểm soát rõ ràng.",
                "Trong đề tài này, mô hình cộng tác người - AI được tổ chức thành hai lớp. Lớp thứ nhất là lifecycle templates, giúp xác định artefact cần có ở từng giai đoạn. Lớp thứ hai là skill suite, giúp đóng gói cách làm thành workflow có vai trò, đầu vào, đầu ra, gate và kiểm chứng. Sự kết hợp này làm giảm độ tùy tiện khi tương tác với chatbot, đồng thời tăng khả năng tái sử dụng cho các dự án sau.",
                "Cách tiếp cận này cũng phù hợp với NIST AI RMF, trong đó rủi ro AI cần được quản lý theo các chức năng như govern, map, measure và manage. Khi áp dụng vào phát triển website, govern tương ứng với quy định vai trò và trách nhiệm; map tương ứng với xác định ngữ cảnh sử dụng AI; measure tương ứng với đo chất lượng output; manage tương ứng với kiểm soát rủi ro, review và cải tiến liên tục.",
            ],
        ),
        (
            "4.2. AI trong phân tích yêu cầu và thiết kế phạm vi website",
            [
                "Phân tích yêu cầu là giai đoạn dễ bị bỏ qua trong các dự án website nhỏ. Nhóm phát triển thường bắt đầu bằng giao diện hoặc code mà chưa làm rõ mục tiêu người dùng, phạm vi nghiệp vụ, luồng chuyển đổi, nội dung cần có và tiêu chí hoàn thành. AI chatbot có thể hỗ trợ bằng cách đặt câu hỏi theo nhiều góc nhìn: người dùng cuối, chủ website, quản trị viên, đội marketing, đội kỹ thuật và đội vận hành.",
                "Trong phase Discovery của bộ template, các artefact như requirements, user stories, use cases và risk analysis giúp chuyển cuộc trao đổi tự do thành dữ liệu có cấu trúc. Khi chatbot nhận được template rõ ràng, đầu ra sẽ ít lan man hơn. Ví dụ, thay vì hỏi “hãy làm website bán hoa”, nhóm có thể yêu cầu AI điền bảng user story gồm vai trò, mục tiêu, lý do, tiêu chí chấp nhận và rủi ro. Nhờ vậy, thông tin có thể được review bởi con người trước khi chuyển sang thiết kế.",
                "AI cũng hữu ích trong việc phát hiện yêu cầu ẩn. Với website thương mại điện tử, chatbot có thể gợi ý các luồng như tìm kiếm sản phẩm, lọc theo dịp tặng, giỏ hàng, thanh toán, email xác nhận, quản lý đơn, chính sách đổi trả, tracking giao hàng và SEO sản phẩm. Với website doanh nghiệp, chatbot có thể gợi ý cấu trúc như giới thiệu, dịch vụ, dự án, đội ngũ, blog, tuyển dụng và liên hệ.",
                "Tuy nhiên, AI không thể tự xác thực nhu cầu thật. Các đề xuất persona hoặc use case của AI có thể hợp lý về mặt ngôn ngữ nhưng sai so với thị trường cụ thể. Vì vậy, output của AI phải được xem là bản nháp để phỏng vấn, khảo sát hoặc xác nhận với stakeholder. Đây là lý do bộ template cần có trường owner, source, evidence và sign-off cho các tài liệu yêu cầu quan trọng.",
            ],
        ),
        (
            "4.3. AI trong lập kế hoạch kiến trúc, sitemap và công nghệ",
            [
                "Giai đoạn Planning biến yêu cầu thành cấu trúc triển khai. Với website, các quyết định quan trọng gồm sitemap, kiến trúc frontend/backend, mô hình dữ liệu, tích hợp API, chiến lược deployment và milestone. AI chatbot có thể tạo nhanh nhiều phương án, so sánh ưu nhược điểm và viết Architecture Decision Record (ADR) để lưu lại lý do lựa chọn.",
                "Điểm mạnh của AI ở planning là khả năng tổng hợp. Khi được cung cấp yêu cầu, ràng buộc ngân sách, năng lực đội ngũ và thời hạn, chatbot có thể đề xuất các stack như Next.js + Payload CMS, Vue + Laravel, WordPress headless hoặc static site generator. Tuy nhiên, lựa chọn công nghệ không nên dựa vào xu hướng mà phải dựa vào năng lực vận hành, bảo mật, khả năng bảo trì và tổng chi phí sở hữu.",
                "Một rủi ro phổ biến khi dùng AI ở planning là mô hình thường đề xuất kiến trúc quá phức tạp. Ví dụ, với website giới thiệu doanh nghiệp nhỏ, việc thêm microservices, message queue hoặc Kubernetes có thể làm tăng chi phí mà không tạo giá trị. Vì vậy, template tech-stack-decision cần yêu cầu AI nêu rõ khi nào không nên dùng một công nghệ, không chỉ nêu ưu điểm.",
                "Bộ skill-planner trong sản phẩm nghiên cứu giải quyết vấn đề này bằng cách tách kế hoạch thành task có dependency và trace. Khi mỗi task đều phải truy về thiết kế gốc, khả năng thêm yêu cầu tùy tiện giảm xuống. Đây là điểm khác biệt giữa việc nhờ chatbot lập kế hoạch tự do và việc dùng một planner skill có hợp đồng đầu ra rõ ràng.",
            ],
        ),
        (
            "4.4. AI trong thiết kế UI/UX, accessibility và design system",
            [
                "Trong thiết kế website, AI có thể hỗ trợ tạo wireframe mô tả bằng văn bản, đề xuất component, tạo checklist responsive, phân tích accessibility và viết đặc tả design system. Các công cụ tạo giao diện bằng prompt như v0, Lovable hoặc các IDE AI có thể rút ngắn thời gian tạo bản nháp. Tuy nhiên, chất lượng UI/UX phụ thuộc vào hiểu biết về người dùng, ngữ cảnh thương hiệu và kiểm thử thực tế.",
                "WCAG 2.2 của W3C là nguồn quan trọng để xây dựng tiêu chí accessibility. WCAG 2.2 bổ sung các tiêu chí liên quan đến focus, target size, dragging movement, consistent help và accessible authentication. Khi dùng AI để sinh giao diện, các tiêu chí này cần được đưa vào prompt và checklist, thay vì chỉ yêu cầu “thiết kế đẹp”.",
                "AI thường tạo giao diện trông hợp lý ở desktop nhưng dễ lỗi ở mobile, thiếu trạng thái focus, contrast yếu, form không có label rõ, hoặc component bị lệ thuộc vào màu sắc để truyền đạt thông tin. Do đó, phase Design trong bộ template có các tài liệu như accessibility.md, responsive-design.md, component-spec.md và design-system.md. Các tài liệu này giúp AI sinh đầu ra có kiểm soát hơn.",
                "Trong thực tế triển khai, AI nên được dùng để tạo nhiều phương án thiết kế và checklist, còn quyết định cuối cùng phải dựa trên review của người dùng, kiểm tra keyboard navigation, screen reader, contrast và khả năng đọc trên thiết bị thật. Nếu có dữ liệu analytics, AI có thể hỗ trợ phân tích điểm rơi trong funnel, nhưng không nên tự kết luận nguyên nhân hành vi người dùng nếu thiếu bằng chứng.",
            ],
        ),
        (
            "4.5. AI trong nội dung, SEO và E-E-A-T",
            [
                "AI chatbot có năng lực mạnh trong việc tạo nháp nội dung: tiêu đề, mô tả sản phẩm, FAQ, metadata, bài blog, nội dung landing page và schema suggestion. Tuy nhiên, Google Search Central nhấn mạnh rằng vấn đề không nằm ở việc nội dung được tạo bằng AI hay con người, mà ở chất lượng, tính hữu ích, độ tin cậy và việc nội dung có được tạo ra chủ yếu cho người đọc hay chỉ để thao túng thứ hạng tìm kiếm.",
                "Vì vậy, ứng dụng AI trong content phải đi kèm nguyên tắc people-first content. Nội dung cần cung cấp thông tin gốc, mô tả đầy đủ chủ đề, có chuyên môn, có nguồn, có trách nhiệm biên tập và không sao chép máy móc. Với website doanh nghiệp, AI có thể tạo bản nháp về dịch vụ nhưng thông tin năng lực, dự án, giá trị khác biệt và cam kết phải được xác nhận bởi doanh nghiệp.",
                "Phase Content trong bộ template gồm content-guidelines, seo-checklist, metadata-template và copywriting-brief. Các tài liệu này giúp AI hiểu giọng văn, mục tiêu chuyển đổi, từ khóa, intent, cấu trúc heading và tiêu chí kiểm duyệt. Một prompt SEO tốt cần yêu cầu AI nêu giả định, nguồn dữ liệu, đối tượng người đọc và đề xuất cách kiểm tra nội dung.",
                "Rủi ro lớn nhất là tạo nội dung hàng loạt nhưng mỏng, lặp lại và thiếu trải nghiệm thực. Nội dung như vậy có thể làm giảm niềm tin người dùng và không bền vững về SEO. Do đó, báo cáo khuyến nghị dùng AI để tăng tốc bản nháp, nhưng luôn cần human edit, kiểm tra sự thật, thêm trải nghiệm thực tế và cập nhật thông tin định kỳ.",
            ],
        ),
        (
            "4.6. AI trong sinh mã nguồn và phát triển frontend/backend",
            [
                "Trong development, chatbot AI có thể hỗ trợ tạo cấu trúc project, component, API handler, schema database, migration, test unit và tài liệu kỹ thuật. Với frontend, AI hữu ích trong việc tạo component theo design system, xử lý state đơn giản, viết form validation và thêm trạng thái loading/error/empty. Với backend, AI có thể gợi ý endpoint, DTO, validation, access control và error handling.",
                "Tuy nhiên, code do AI tạo ra có thể chạy được nhưng không phù hợp với kiến trúc dự án. Lỗi thường gặp gồm import sai, xử lý exception thiếu, bỏ qua edge cases, thiếu kiểm soát quyền truy cập, lộ secret, query không tối ưu và không phù hợp coding convention. Vì vậy, phase Development của bộ template có coding-standards, api-design, database-schema, deployment-strategy và git-workflow.",
                "Các nghiên cứu về code generation cho thấy năng lực sinh code đã tiến bộ rõ rệt từ Codex đến các mô hình hiện đại, nhưng đánh giá vẫn cần dựa trên test. HumanEval đo khả năng giải bài lập trình nhỏ, trong khi SWE-bench đo khả năng sửa lỗi trong repo thực tế. Hai benchmark này đều hữu ích nhưng không thay thế kiểm thử trong dự án cụ thể.",
                "Quy trình khuyến nghị là: AI tạo bản nháp, lập trình viên review, chạy test, lint, type check, security scan, sau đó mới merge. Với các module quan trọng như thanh toán, xác thực, phân quyền, quản lý dữ liệu cá nhân, AI không nên được phép tự triển khai mà không có review nghiêm ngặt. Skill-builder trong đề tài được thiết kế theo hướng này: đọc design và todo, triển khai theo phase, ghi build-log và kiểm tra placeholder.",
            ],
        ),
        (
            "4.7. AI trong kiểm thử, bảo mật và kiểm soát chất lượng",
            [
                "Testing là giai đoạn AI có thể mang lại giá trị rõ ràng nếu được dùng đúng cách. Chatbot có thể sinh test case từ user story, tạo checklist regression, viết test unit, gợi ý test e2e, tạo bug report và phân loại mức độ nghiêm trọng. Với website, AI có thể giúp nghĩ đến các trường hợp như form bỏ trống, dữ liệu quá dài, ký tự đặc biệt, lỗi mạng, role không đủ quyền và trạng thái session hết hạn.",
                "Tuy vậy, AI-generated tests thường thiên về happy path và dễ bỏ sót edge cases. Nếu prompt không yêu cầu rõ, AI có thể tạo test chỉ xác nhận component render mà không kiểm tra hành vi quan trọng. Vì vậy, phase Testing trong bộ template có browser-automation-test-plan, performance-checklist, security-checklist, bug-report và test-plan. Các tài liệu này giúp biến kiểm thử thành artefact có thể review.",
                "Về bảo mật LLM, OWASP Top 10 for LLM Applications nhấn mạnh prompt injection là một trong các rủi ro hàng đầu. Với website tích hợp chatbot, rủi ro không chỉ là lỗi code mà còn là việc người dùng nhập prompt độc hại để làm lộ dữ liệu, vượt chính sách hoặc thao túng hành vi agent. Do đó, chatbot cần giới hạn quyền, tách dữ liệu nhạy cảm, kiểm soát tool access và log tương tác.",
                "Đối với website truyền thống, bảo mật vẫn bao gồm xác thực, phân quyền, bảo vệ API, chống injection, CSRF/XSS, quản lý secret, rate limiting và kiểm soát upload file. AI có thể giúp rà checklist nhưng không thay thế threat modeling và security review. Báo cáo đề xuất mọi workflow AI có quyền sửa code hoặc gọi tool phải có nguyên tắc least privilege và cơ chế human approval ở bước rủi ro cao.",
            ],
        ),
        (
            "4.8. AI trong hiệu năng, Core Web Vitals và PWA",
            [
                "Hiệu năng website ảnh hưởng trực tiếp đến trải nghiệm người dùng, SEO và tỷ lệ chuyển đổi. Các chỉ số Core Web Vitals như LCP, INP và CLS giúp đánh giá tốc độ tải, độ phản hồi và ổn định giao diện. AI chatbot có thể hỗ trợ đọc báo cáo Lighthouse, giải thích nguyên nhân LCP cao, gợi ý tối ưu ảnh, lazy loading, code splitting, caching và giảm JavaScript không cần thiết.",
                "Tuy nhiên, tối ưu hiệu năng cần đo trên môi trường thật. AI không thể biết bundle size, waterfall network, server response time hoặc thiết bị người dùng nếu không được cung cấp dữ liệu. Vì vậy, template performance-baseline và performance-report trong phase Maintenance yêu cầu lưu metric, bối cảnh đo, công cụ đo, phiên bản build và owner.",
                "Với PWA, MDN mô tả các thành phần như web app manifest, service worker, cache và khả năng offline. AI có thể tạo manifest, gợi ý caching strategy và viết service worker đơn giản. Nhưng service worker dễ gây lỗi cache stale, update không đúng hoặc hoạt động khác nhau giữa trình duyệt. Do đó, PWA cần test cẩn thận các trường hợp install, offline, update và fallback.",
                "Trong workflow đề xuất, AI được dùng để tạo checklist hiệu năng và giải pháp tối ưu ban đầu; con người cung cấp số liệu đo thật và quyết định trade-off. Ví dụ, tăng animation có thể làm giao diện hấp dẫn nhưng giảm performance trên thiết bị yếu. Tối ưu đúng cần cân bằng trải nghiệm, hiệu năng, bảo trì và mục tiêu kinh doanh.",
            ],
        ),
        (
            "4.9. AI agents và workflow chuyên biệt cho phát triển website",
            [
                "Xu hướng mới không chỉ là chatbot trả lời câu hỏi mà là AI agents có khả năng dùng tool, đọc file, chỉnh code, chạy test và ghi log. Trong bối cảnh website, agent có thể đóng vai trò chuyên biệt như requirements analyst, UI reviewer, SEO assistant, test generator, accessibility auditor hoặc deployment checker. Tuy nhiên, agent càng có nhiều quyền thì rủi ro càng lớn.",
                "Bộ skill architect-planner-builder của đề tài là bước cụ thể hóa khái niệm agent thành workflow có kiểm soát. Skill-architect thiết kế cấu trúc và rủi ro; skill-planner phân rã task và tài nguyên; skill-builder triển khai theo hợp đồng zone mapping. Nhờ vậy, mỗi agent không hành động tự do mà phải theo tài liệu nguồn.",
                "Một lợi ích quan trọng của cách đóng gói skill là chuyển tri thức chuyên gia thành tài sản tái sử dụng. Nếu một nhóm đã có quy trình tốt để review UI, họ có thể biến quy trình đó thành skill với checklist, templates và guardrails. Khi dự án mới bắt đầu, skill có thể được gọi lại thay vì giải thích từ đầu.",
                "Tuy nhiên, agent workflow cần có cơ chế dừng. Những bước như xóa file, thay đổi API public, cập nhật database schema, deploy production hoặc xử lý dữ liệu cá nhân phải yêu cầu xác nhận. Đây là nguyên tắc an toàn quan trọng khi đưa AI vào phát triển website thực tế.",
            ],
        ),
        (
            "4.10. Đề xuất bộ tiêu chí đánh giá ứng dụng AI trong phát triển website",
            [
                "Để đánh giá nghiêm túc hiệu quả của AI trong phát triển website, không nên chỉ hỏi cảm nhận 'nhanh hơn hay không'. Cần có bộ tiêu chí gồm định lượng và định tính. Định lượng có thể gồm thời gian từng phase, số lần sửa lại, số bug, test coverage, Lighthouse score, số lỗi accessibility, số lỗi security và số incident sau triển khai.",
                "Định tính có thể gồm mức hài lòng của developer, độ dễ hiểu của code, mức phù hợp với yêu cầu, khả năng bảo trì, độ rõ của tài liệu và mức tin cậy của stakeholder. Với AI, cần thêm tiêu chí riêng như hallucination rate, số output phải reject, mức đầy đủ của trace, chất lượng prompt và mức độ cần human intervention.",
                "Một thiết kế pilot khả thi cho sinh viên là chọn một website nhỏ, ví dụ landing page hoặc catalog sản phẩm, sau đó triển khai hai vòng: vòng không dùng workflow AI có cấu trúc và vòng dùng template + skill. Mỗi vòng ghi log thời gian, task, lỗi, số lần sửa và output. Dữ liệu này chưa đủ để kết luận phổ quát, nhưng đủ để minh họa tác động của framework.",
                "Nếu muốn đạt chuẩn nghiên cứu cao hơn, cần có nhóm đối chứng, cùng task, cùng thời lượng, cùng tiêu chí chấm và nhiều người tham gia. Cách làm này tương tự tinh thần của Peng et al. (2023), nhưng có thể thu nhỏ phù hợp với điều kiện đề tài sinh viên. Quan trọng nhất là không biến cảm nhận hoặc ước tính nội bộ thành kết luận định lượng chắc chắn.",
            ],
        ),
    ]
    for title, paragraphs in sections:
        new_body.append(paragraph(title, bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
        for p in paragraphs:
            new_body.append(paragraph(p, after=120, size=26))

    new_body.append(paragraph("CHƯƠNG 5. PHÂN TÍCH CHI TIẾT 7 GIAI ĐOẠN WEBSITE LIFECYCLE VỚI AI CHATBOT", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    phase_details = [
        ("5.1. Discovery", "Discovery là nền tảng của toàn bộ dự án. Khi dùng AI ở giai đoạn này, mục tiêu không phải là tạo ngay giao diện hay code, mà là làm rõ vấn đề cần giải quyết. Chatbot có thể hỏi về đối tượng người dùng, hành trình chính, mục tiêu chuyển đổi, dữ liệu cần quản lý, các bên liên quan và rủi ro. Bộ template requirements, user-stories, use-cases và risk-analysis giúp chuẩn hóa câu trả lời thành tài liệu có thể kiểm tra. Đầu ra tốt của Discovery phải đủ rõ để người khác đọc vào hiểu website phục vụ ai, giải quyết vấn đề gì, thành công được đo ra sao và điều gì nằm ngoài phạm vi."),
        ("5.2. Planning", "Planning chuyển yêu cầu thành kế hoạch triển khai. AI có thể đề xuất sitemap, ADR, milestone, API plan và tech stack. Tuy nhiên, quyết định cuối cùng cần dựa vào bối cảnh đội ngũ. Một website nhỏ có thể không cần kiến trúc phức tạp; ngược lại, website có thanh toán, tài khoản, dữ liệu cá nhân và tích hợp bên thứ ba cần thiết kế bảo mật nghiêm túc. Template architecture-decision-record giúp lưu lại lý do chọn hoặc không chọn một giải pháp, tránh quyết định theo cảm tính hoặc xu hướng."),
        ("5.3. Design", "Design với AI nên bắt đầu từ design system và component spec, không chỉ từ hình ảnh đẹp. AI có thể tạo token màu, typography scale, spacing, trạng thái component và checklist accessibility. Sau đó, người thiết kế kiểm tra lại contrast, focus, responsive và consistency. Khi prompt chỉ yêu cầu 'làm đẹp', AI thường tạo UI chung chung; khi prompt dựa trên component spec và accessibility checklist, output có khả năng dùng thực tế cao hơn."),
        ("5.4. Content", "Content là nơi AI có thể tiết kiệm nhiều thời gian nhưng cũng dễ tạo rủi ro chất lượng. AI có thể tạo bản nháp mô tả sản phẩm, FAQ, metadata và nội dung landing page. Tuy nhiên, nội dung cần được kiểm tra theo tiêu chí helpful, reliable, people-first. Với website dùng trong kinh doanh, thông tin sản phẩm, giá, chính sách, điều khoản và lời cam kết phải được xác thực. Template content-guidelines và seo-checklist giúp quy định giọng văn, cấu trúc heading, search intent và tiêu chí biên tập."),
        ("5.5. Development", "Development là phase dễ bị lạm dụng AI nhất. AI có thể tạo nhanh nhiều code, nhưng code nhanh không đồng nghĩa code đúng. Quy trình an toàn là yêu cầu AI làm từng phần nhỏ, giải thích giả định, tạo test đi kèm, và không tự ý thay đổi kiến trúc. Template coding-standards, api-design và database-schema giúp ràng buộc AI vào pattern dự án. Mọi output cần qua type check, lint, test và review trước khi merge."),
        ("5.6. Testing", "Testing giúp biến AI từ công cụ tạo code thành công cụ nâng chất lượng. AI có thể sinh test case từ use case và acceptance criteria, nhưng con người cần đánh giá edge cases. Test plan phải bao gồm unit, integration, e2e, browser compatibility, accessibility, performance và security. Với website, test không chỉ kiểm tra function đúng mà còn kiểm tra người dùng có hoàn thành mục tiêu được không. Browser automation test plan giúp lưu evidence thay vì chỉ nói 'đã test'."),
        ("5.7. Maintenance", "Maintenance là giai đoạn chứng minh website có sống được sau khi deploy hay không. AI có thể hỗ trợ viết incident report, phân tích log, tạo changelog, gợi ý cải tiến performance và lập kế hoạch refactor. Nhưng vận hành cần số liệu thật: uptime, error rate, Core Web Vitals, ticket người dùng, incident và chi phí. Template maintenance-log, incident-report, performance-baseline và performance-report giúp quá trình cải tiến có bằng chứng."),
    ]
    for title, body in phase_details:
        new_body.append(paragraph(title, bold=True, justify=False, page_break=True, before=120, after=120, size=26, keep_next=True))
        for i in range(3):
            if i == 0:
                text = body
            elif i == 1:
                text = "Trong workflow đề xuất, chatbot AI được cấp vai trò cụ thể cho phase này: tạo bản nháp, kiểm tra checklist, phát hiện thiếu sót và đề xuất câu hỏi tiếp theo. Output của AI không được xem là bản cuối ngay lập tức mà phải đi qua review, đối chiếu với template và lưu evidence. Cách làm này giúp giảm lỗi do prompt mơ hồ và tăng tính nhất quán giữa các dự án."
            else:
                text = "Giá trị tối ưu hóa của phase này nằm ở khả năng giảm thời gian chuẩn bị artefact, tăng độ đầy đủ của tài liệu và tạo nền tảng cho phase tiếp theo. Nếu thiếu phase này, các bước sau có thể nhanh hơn ở bề mặt nhưng dễ phát sinh lỗi sửa lại. Vì vậy, tối ưu bằng AI không phải là bỏ qua quy trình, mà là làm quy trình nhanh hơn, rõ hơn và dễ kiểm chứng hơn."
            new_body.append(paragraph(text, after=120, size=26))

    new_body.append(paragraph("CHƯƠNG 6. THIẾT KẾ PILOT VÀ HƯỚNG ĐÁNH GIÁ THỰC NGHIỆM", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    pilot_sections = [
        (
            "6.1. Lý do cần thiết kế pilot thay vì kết luận định lượng ngay",
            [
                "Một điểm quan trọng khi nghiên cứu ứng dụng AI chatbot trong phát triển website là không được nhầm lẫn giữa cảm nhận năng suất và bằng chứng năng suất. Khi một lập trình viên dùng AI và cảm thấy công việc nhanh hơn, điều đó có giá trị kinh nghiệm nhưng chưa đủ để kết luận khoa học. Để kết luận rằng AI giúp giảm một tỷ lệ phần trăm thời gian cụ thể, nhóm nghiên cứu cần log thời gian, mô tả task, tiêu chí đánh giá, số lần sửa lỗi, số lượng người tham gia và điều kiện so sánh.",
                "Các nghiên cứu quốc tế có độ tin cậy cao thường thiết kế thí nghiệm có kiểm soát. Peng et al. (2023) không kết luận chung chung rằng AI luôn tăng năng suất, mà đo một tác vụ cụ thể với nhóm dùng Copilot và nhóm không dùng Copilot. Vaithilingam et al. (2022) cũng không chỉ dựa vào cảm nhận, mà quan sát người tham gia khi dùng Copilot, phân tích khó khăn trong hiểu và sửa code. Những cách làm này cho thấy nghiên cứu về AI cần mô tả rõ bối cảnh và giới hạn.",
                "Với phạm vi đề tài sinh viên, cách phù hợp là thiết kế pilot nhỏ nhưng có dữ liệu. Pilot không cần bao phủ toàn bộ ngành web development, nhưng phải ghi lại đủ bằng chứng cho một số tác vụ đại diện. Ví dụ, nhóm có thể chọn một landing page, một trang catalog sản phẩm và một API đơn giản để so sánh quy trình truyền thống với quy trình dùng lifecycle templates + skill suite.",
                "Khi chuyển các con số như 36,3% hoặc 35% thành mục tiêu/pilot thay vì kết luận chắc chắn, báo cáo trở nên đáng tin hơn. Điều này không làm giảm giá trị đề tài; ngược lại, nó thể hiện thái độ nghiên cứu nghiêm túc. Đóng góp chính hiện tại là framework và sản phẩm hỗ trợ workflow, còn định lượng hiệu quả là bước cần đo tiếp bằng pilot có kiểm chứng.",
            ],
        ),
        (
            "6.2. Thiết kế pilot đề xuất cho một website mẫu",
            [
                "Pilot đề xuất gồm một website mẫu có phạm vi vừa đủ: trang chủ, trang danh sách sản phẩm/dịch vụ, trang chi tiết, form liên hệ và khu vực quản trị đơn giản. Website không nên quá nhỏ đến mức AI không có đất thể hiện, nhưng cũng không nên quá lớn khiến việc đo lường vượt quá nguồn lực. Một ví dụ phù hợp là website bán hoa, website dịch vụ sửa chữa hoặc website giới thiệu doanh nghiệp nhỏ.",
                "Pilot có thể chia thành hai vòng. Vòng A thực hiện theo cách thông thường: người thực hiện tự thu thập yêu cầu, tự lập kế hoạch và dùng AI tự do nếu cần. Vòng B dùng bộ Website Lifecycle Templates và skill suite: Discovery tạo requirements/user stories/risk analysis; Planning tạo sitemap/ADR/roadmap; Design tạo component spec/accessibility checklist; Development tạo API/component theo coding standards; Testing tạo test plan và bug report; Maintenance tạo performance baseline.",
                "Để so sánh công bằng, hai vòng cần có cùng phạm vi chức năng và cùng tiêu chí hoàn thành. Nếu chỉ vòng B được review kỹ hơn, kết quả sẽ thiên lệch. Ngược lại, nếu vòng A dùng công cụ khác mà vòng B không dùng, kết luận cũng không rõ. Vì vậy, pilot nên ghi rõ công cụ được phép, thời gian tối đa, tài liệu đầu vào, người review và cách chấm điểm.",
                "Đầu ra của pilot không nhất thiết phải là website production hoàn chỉnh. Với đề tài NCKH sinh viên, có thể dừng ở mức prototype có repo, tài liệu, test report và Lighthouse report. Điều quan trọng là chứng minh framework giúp quy trình rõ hơn, output đầy đủ hơn và lỗi dễ phát hiện hơn. Đây là bằng chứng phù hợp hơn so với việc đưa ra số liệu phần trăm không có log.",
            ],
        ),
        (
            "6.3. Hệ thống chỉ số đo lường",
            [
                "Chỉ số đầu tiên là thời gian. Nhóm cần ghi thời gian cho từng phase: discovery, planning, design, content, development, testing, maintenance. Thời gian nên được log theo task nhỏ, ví dụ 'viết user stories', 'tạo sitemap', 'xây component product card', 'viết test form liên hệ'. Cách log theo phase giúp biết AI hỗ trợ mạnh ở đâu và yếu ở đâu, thay vì chỉ có một tổng thời gian mơ hồ.",
                "Chỉ số thứ hai là chất lượng artefact. Với requirements, có thể chấm theo mức đầy đủ của mục tiêu, persona, use case, acceptance criteria và risk. Với code, có thể chấm theo test pass, lint/type check, bug report, maintainability và security review. Với UI, có thể chấm theo responsive, accessibility, consistency và usability. Với content, có thể chấm theo tính đúng, hữu ích, nguồn và giọng văn.",
                "Chỉ số thứ ba là mức kiểm soát AI. Đây là điểm riêng của đề tài. Nhóm có thể đo số lần AI tạo output sai nguồn, số lần phải sửa do hallucination, số prompt phải viết lại, số output có trace, số checklist pass/fail và số lần cần human approval. Những chỉ số này phản ánh giá trị của skill suite vì mục tiêu của nó là giảm hành vi AI thiếu kiểm soát.",
                "Chỉ số thứ tư là trải nghiệm người thực hiện. Sau mỗi vòng pilot, người thực hiện có thể tự đánh giá mức dễ hiểu, mức tự tin khi sử dụng output AI, mức công sức review và mức sẵn sàng dùng lại workflow. Các đánh giá này không thay thế số liệu kỹ thuật nhưng giúp giải thích tại sao một workflow hiệu quả hoặc không hiệu quả trong thực tế.",
            ],
        ),
        (
            "6.4. Quy trình thu thập và lưu evidence",
            [
                "Một nghiên cứu ứng dụng AI tốt cần evidence. Với phát triển website, evidence gồm repo Git, commit history, prompt log, output của AI, checklist đã điền, screenshot, test report, Lighthouse report, bug report và quyết định kiến trúc. Nếu thiếu evidence, người đọc không thể phân biệt giữa kết quả thật và mô tả sau khi sự việc đã xảy ra.",
                "Bộ template trong đề tài có thể được mở rộng bằng trường evidence cho các tài liệu quan trọng. Ví dụ, test-plan nên có link tới test output; performance-report nên có ngày đo, URL, thiết bị, network profile và công cụ đo; ADR nên có người quyết định và phương án bị loại; bug-report nên có steps to reproduce và expected/actual result. Khi AI tạo tài liệu, các trường này buộc người dùng cung cấp dữ liệu thật.",
                "Đối với prompt log, nhóm nên lưu prompt đầu vào, model/tool sử dụng, ngày chạy và output chính. Việc này giúp audit lại khi kết quả sai. Tuy nhiên, prompt log không được chứa secret, token, dữ liệu cá nhân hoặc thông tin nội bộ nhạy cảm. Nếu có dữ liệu nhạy cảm, cần sanitize trước khi đưa vào AI cloud service.",
                "Skill-builder trong bộ skill có build-log, đây là hướng đúng cho evidence. Mỗi task nên ghi nguồn dữ liệu, file tạo ra, quyết định quan trọng và kết quả validation. Khi áp dụng vào website, build-log có thể trở thành nhật ký kỹ thuật giúp người sau hiểu vì sao một component, API hoặc checklist được tạo như vậy.",
            ],
        ),
        (
            "6.5. Kịch bản áp dụng trong đào tạo và doanh nghiệp nhỏ",
            [
                "Trong đào tạo, framework này giúp sinh viên không chỉ học cách hỏi AI mà học cách tổ chức quy trình phát triển phần mềm. Mỗi nhóm sinh viên có thể được giao cùng một đề bài website và bắt buộc tạo artefact theo 7 phase. Chatbot AI được dùng để hỗ trợ tạo bản nháp, nhưng sinh viên phải review, sửa, dẫn nguồn và giải thích quyết định. Cách làm này giúp phát triển cả kỹ năng kỹ thuật lẫn tư duy phản biện.",
                "Giảng viên có thể chấm theo artefact thay vì chỉ chấm sản phẩm cuối. Ví dụ, requirements có rõ không, ADR có hợp lý không, design system có nhất quán không, test plan có bao phủ edge cases không, report có evidence không. AI khi đó trở thành công cụ học tập có kiểm soát, không phải công cụ làm hộ.",
                "Với doanh nghiệp nhỏ, giá trị nằm ở khả năng chuẩn hóa quy trình mà không cần đội ngũ lớn. Một chủ doanh nghiệp có thể dùng Discovery template để mô tả nhu cầu, dùng Content template để chuẩn bị nội dung, dùng Planning template để làm việc với freelancer hoặc agency, và dùng Maintenance template để theo dõi sau khi website chạy. AI chatbot giúp điền bản nháp, nhưng chủ doanh nghiệp vẫn giữ quyền xác nhận.",
                "Đối với nhóm phát triển chuyên nghiệp, bộ skill có thể dùng để tạo các workflow chuyên biệt như SEO content generator, API documentation writer, UI accessibility reviewer hoặc test-case generator. Mỗi workflow nếu được đóng gói thành skill sẽ giảm thời gian onboarding và giảm phụ thuộc vào kinh nghiệm cá nhân của từng thành viên.",
            ],
        ),
        (
            "6.6. Giới hạn và hướng phát triển tiếp theo",
            [
                "Giới hạn đầu tiên của đề tài là chưa có thí nghiệm quy mô lớn. Các kết quả sản phẩm đã rõ nhưng hiệu quả định lượng cần đo tiếp. Giới hạn thứ hai là các nguồn benchmark quốc tế chủ yếu đo coding task, chưa đo đầy đủ toàn bộ lifecycle website. Vì vậy, khi áp dụng vào website, cần thận trọng và không suy rộng quá mức.",
                "Giới hạn thứ ba là chất lượng AI thay đổi nhanh theo thời gian. Một prompt hoặc workflow hiệu quả hôm nay có thể cần điều chỉnh khi model mới ra đời. Do đó, bộ template và skill nên được versioning, có ngày cập nhật và có checklist review định kỳ. Đây là lý do trong báo cáo có nhấn mạnh metadata, status và verified date.",
                "Hướng phát triển tiếp theo là bổ sung monitoring/alerting runbook, dependency update runbook, i18n/compliance checklist và mock strategy cho testing. Các nội dung này đã được ghi nhận là follow-up trong bộ website-lifecycle-templates. Khi bổ sung, framework sẽ bao phủ tốt hơn các dự án production.",
                "Một hướng khác là xây dựng dashboard đo workflow AI: số prompt, số output pass checklist, số lỗi phát hiện, thời gian từng phase, số lần human intervention và mức tiết kiệm thời gian. Nếu có dashboard, đề tài có thể chuyển từ nghiên cứu thiết kế artefact sang nghiên cứu thực nghiệm có dữ liệu mạnh hơn.",
            ],
        ),
    ]
    for title, paragraphs in pilot_sections:
        new_body.append(paragraph(title, bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
        for p in paragraphs:
            new_body.append(paragraph(p, after=120, size=26))

    new_body.append(paragraph("PHỤ LỤC 2. INVENTORY CHI TIẾT BỘ WEBSITE LIFECYCLE TEMPLATES", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    inventory_intro = [
        "Phụ lục này liệt kê các nhóm tài liệu chính trong bộ Website Lifecycle Templates. Mục đích là chứng minh sản phẩm nghiên cứu không chỉ là mô tả khái niệm mà đã có cấu trúc tài liệu cụ thể, có thể dùng để hỗ trợ chatbot AI trong từng giai đoạn phát triển website.",
        "Các artefact được chia thành bốn loại: templates là tài liệu/checklist có thể copy dùng ngay; prompts là chỉ dẫn cho AI tools; patterns là best practices hoặc workflow tái sử dụng; examples là ví dụ đầu ra. Cách tổ chức này giúp chatbot có nguồn ngữ cảnh rõ ràng, đồng thời giúp người dùng đánh giá output theo từng loại artefact.",
    ]
    for p in inventory_intro:
        new_body.append(paragraph(p, after=120, size=26))
    inventory_rows = [["Phase", "Nhóm", "File / Artefact", "Cách dùng trong nghiên cứu"]]
    base = Path("website-lifecycle-templates")
    if base.exists():
        for file in sorted(base.glob("[1-7]-*/*/*.md")):
            parts = file.parts
            phase = parts[1]
            group = parts[2]
            name = parts[3]
            use = {
                "templates": "Đầu ra chuẩn để AI điền hoặc nhóm dự án sử dụng",
                "prompts": "Prompt mẫu giúp AI tạo bản nháp theo phase",
                "patterns": "Quy trình/best practice để kiểm soát chất lượng",
                "examples": "Minh họa output và cách áp dụng template",
            }.get(group, "Tài liệu hỗ trợ")
            inventory_rows.append([phase, group, name, use])
    new_body.append(table(inventory_rows[:55]))
    if len(inventory_rows) > 55:
        new_body.append(paragraph("Bảng tiếp theo liệt kê phần còn lại của inventory để phục vụ đối chiếu và kiểm tra.", italic=True, after=120, size=26))
        new_body.append(table([inventory_rows[0]] + inventory_rows[55:110]))

    new_body.append(paragraph("PHỤ LỤC 3. MA TRẬN RỦI RO KHI ỨNG DỤNG AI CHATBOT TRONG PHÁT TRIỂN WEBSITE", bold=True, center=True, justify=False, page_break=True, before=120, after=240, size=28))
    risk_rows = [
        ["Rủi ro", "Biểu hiện", "Tác động", "Biện pháp kiểm soát"],
        ["Hallucination", "AI bịa API, thư viện, số liệu hoặc citation", "Sai thiết kế, sai báo cáo, mất uy tín", "Yêu cầu nguồn, kiểm tra tài liệu gốc, trace output"],
        ["Prompt injection", "Người dùng hoặc dữ liệu ngoài chèn lệnh độc hại", "Lộ dữ liệu, hành động ngoài ý muốn", "Giới hạn tool, lọc input, phân quyền, human approval"],
        ["Code không an toàn", "Thiếu auth, validation, rate limit, escape output", "Lỗ hổng bảo mật", "Security checklist, review, SAST/DAST"],
        ["Nội dung SEO mỏng", "AI tạo bài lặp lại, thiếu trải nghiệm thực", "Giảm chất lượng và độ tin cậy", "People-first content, biên tập người thật, nguồn rõ"],
        ["Thiếu accessibility", "Không có label, focus, contrast, keyboard support", "Người dùng khuyết tật khó tiếp cận", "WCAG 2.2 checklist và test thủ công"],
        ["Sai kiến trúc", "AI đề xuất stack quá phức tạp hoặc không phù hợp", "Tăng chi phí, khó bảo trì", "ADR, tech-stack decision, review của người phụ trách"],
        ["Phụ thuộc nhà cung cấp", "Workflow chỉ chạy với một model/tool", "Rủi ro chi phí và gián đoạn", "Multi-model strategy, abstraction, fallback manual"],
        ["Thiếu dữ liệu đo lường", "Kết luận năng suất bằng cảm nhận", "Không đủ cơ sở học thuật", "Log thời gian, test report, repo, dashboard"],
    ]
    new_body.append(table(risk_rows))


def add_research_products(new_body):
    new_body.append(paragraph("3.7. Kết quả xây dựng bộ tài liệu Website Lifecycle Templates", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    new_body.append(paragraph(
        "Một kết quả quan trọng của đề tài là bộ tài liệu Website Lifecycle Templates, được thiết kế như một khung làm việc thực dụng cho toàn bộ vòng đời xây dựng website. Bộ tài liệu này không chỉ là tập hợp biểu mẫu rời rạc mà là một hệ thống artefact có cấu trúc, giúp chatbot AI có đủ ngữ cảnh để hỗ trợ từng giai đoạn từ thu thập yêu cầu đến bảo trì sau triển khai.",
        after=120,
        size=26,
    ))
    lifecycle_rows = [
        ["Giai đoạn", "Mục tiêu", "Artefact tiêu biểu"],
        ["Discovery", "Thu thập yêu cầu, user stories, use cases và rủi ro", "requirements, user stories, use cases, risk analysis"],
        ["Planning", "Lập sitemap, kiến trúc, milestone, tech stack và API/integration", "ADR, sitemap, roadmap, tech stack decision"],
        ["Design", "Thiết kế UI/UX, design system, responsive và accessibility", "design system, component spec, accessibility checklist"],
        ["Content", "Xây dựng chiến lược nội dung, SEO, metadata và copywriting", "SEO checklist, metadata template, copywriting brief"],
        ["Development", "Chuẩn hóa phát triển frontend/backend, API, database và deploy", "API design, database schema, coding standards"],
        ["Testing", "Kiểm thử chức năng, trình duyệt, hiệu năng, bảo mật và launch", "test plan, security checklist, performance checklist"],
        ["Maintenance", "Bảo trì, xử lý incident, baseline hiệu năng và yêu cầu tính năng mới", "maintenance log, incident report, performance baseline"],
    ]
    new_body.append(table(lifecycle_rows))
    new_body.append(paragraph(
        "Inventory đã được hệ thống hóa gồm 33 templates, 17 prompts, 20 patterns và 22 examples. Mỗi phase có cùng cấu trúc gồm templates, prompts, patterns và examples. Cách tổ chức này giúp người dùng và AI chatbot có thể nhanh chóng chọn đúng loại tài liệu cần tạo, tránh tình trạng prompt chung chung hoặc thiếu dữ liệu đầu vào.",
        after=120,
        size=26,
    ))

    new_body.append(paragraph("3.8. Kết quả xây dựng bộ skill thiết kế và triển khai workflow AI", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    new_body.append(paragraph(
        "Ngoài bộ template cho vòng đời website, đề tài còn xây dựng bộ skill gồm skill-architect, skill-planner và skill-builder. Đây là sản phẩm thể hiện hướng tiếp cận agent hóa chatbot AI: thay vì để chatbot phản hồi tự do, mỗi skill được ràng buộc bởi vai trò, hợp đồng đầu vào/đầu ra, progressive disclosure, guardrails và cơ chế kiểm chứng chất lượng.",
        after=120,
        size=26,
    ))
    skill_rows = [
        ["Thành phần", "Chức năng", "Cơ chế kiểm soát", "Kết quả"],
        ["skill-architect", "Phân tích yêu cầu và thiết kế kiến trúc skill", "Gate xác nhận, 3 Pillars, 7 Zones, Mermaid diagrams", "design.md"],
        ["skill-planner", "Chuyển thiết kế thành kế hoạch triển khai", "Trace tag, audit tài nguyên, dependency detection", "todo.md"],
        ["skill-builder", "Triển khai skill theo thiết kế và kế hoạch", "Zone Contract, build-log, placeholder scale, validation", "Skill hoàn chỉnh"],
    ]
    new_body.append(table(skill_rows))
    new_body.append(paragraph(
        "Pipeline của bộ skill có dạng: người dùng mô tả nhu cầu, skill-architect tạo design.md, skill-planner tạo todo.md, sau đó skill-builder triển khai skill hoàn chỉnh và ghi build-log. Cấu trúc này làm giảm rủi ro ảo giác của AI vì mọi bước đều có nguồn tham chiếu, trace và tiêu chí kiểm tra.",
        after=120,
        size=26,
    ))

    new_body.append(paragraph("3.9. Mô hình tích hợp hai sản phẩm vào quy trình xây dựng website", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    new_body.append(paragraph(
        "Hai sản phẩm nghiên cứu có vai trò bổ trợ cho nhau. Website Lifecycle Templates cung cấp nội dung, biểu mẫu và chuẩn đầu ra cho từng giai đoạn xây dựng website; bộ skill architect-planner-builder cung cấp phương pháp biến các yêu cầu đó thành workflow AI có kiểm soát. Khi kết hợp, chatbot AI có thể vừa hiểu đúng ngữ cảnh website lifecycle, vừa thực thi theo quy trình có kiểm chứng.",
        after=120,
        size=26,
    ))
    integration_rows = [
        ["Lớp", "Vai trò trong hệ thống", "Tác động tối ưu hóa"],
        ["Lifecycle Templates", "Chuẩn hóa artefact cho 7 giai đoạn website", "Giảm thời gian tạo tài liệu, tăng tính nhất quán"],
        ["Prompts và Patterns", "Hướng dẫn AI tạo, kiểm tra và cải thiện đầu ra", "Giảm prompt mơ hồ, tăng chất lượng phản hồi"],
        ["Skill Suite", "Đóng gói workflow thành các agent có vai trò rõ", "Giảm lỗi quy trình, tăng khả năng tái sử dụng"],
        ["Guardrails và Logs", "Theo dõi quyết định, kiểm tra placeholder, trace nguồn", "Giảm rủi ro ảo giác và sai lệch yêu cầu"],
    ]
    new_body.append(table(integration_rows))
    new_body.append(paragraph(
        "Mô hình tích hợp này cho phép mở rộng sang các workflow chuyên biệt như landing-page-builder, ui-reviewer, api-from-ui, seo-content-generator hoặc form-validator. Mỗi workflow mới có thể sử dụng template của phase tương ứng làm tri thức đầu vào và sử dụng pipeline skill để thiết kế, lập kế hoạch, triển khai, kiểm chứng.",
        after=120,
        size=26,
    ))

    new_body.append(paragraph("3.10. Đánh giá giá trị nghiên cứu và khả năng áp dụng", bold=True, justify=False, before=180, after=120, size=26, keep_next=True))
    value_rows = [
        ["Tiêu chí", "Kết quả đạt được", "Ý nghĩa"],
        ["Tính hệ thống", "7 phase, 4 nhóm artefact mỗi phase", "Bao phủ toàn bộ vòng đời website"],
        ["Tính tái sử dụng", "Template, prompt, pattern, example có cấu trúc thống nhất", "Dễ áp dụng cho nhiều dự án website"],
        ["Tính kiểm soát", "Skill pipeline có gate, trace, log và validation", "Giảm phụ thuộc vào phản hồi tự do của chatbot"],
        ["Tính mở rộng", "Có thể tạo thêm skill chuyên biệt theo từng kỹ năng", "Phù hợp với phát triển website bằng AI agent"],
        ["Tính giáo dục", "Cung cấp quy trình và artefact học tập rõ ràng", "Hỗ trợ sinh viên hiểu cách cộng tác với AI"],
    ]
    new_body.append(table(value_rows))
    new_body.append(paragraph(
        "Từ góc độ nghiên cứu, đóng góp chính của đề tài không chỉ nằm ở việc sử dụng chatbot AI để sinh mã nguồn, mà ở việc xây dựng một hệ sinh thái tài liệu và skill giúp chatbot hoạt động như một cộng sự có quy trình. Đây là khác biệt quan trọng so với cách dùng AI đơn lẻ: hệ thống đề xuất tập trung vào chuẩn hóa đầu vào, kiểm soát quá trình và kiểm chứng đầu ra.",
        after=120,
        size=26,
    ))


def update_numbering(xml_bytes):
    root = ET.fromstring(xml_bytes)
    existing = {n.get(attr("numId")) for n in root.findall("w:num", NS)}
    if "9" not in existing:
        abstract = w_el("abstractNum", {attr("abstractNumId"): "9"})
        lvl = w_el("lvl", {attr("ilvl"): "0"})
        lvl.append(w_el("start", {attr("val"): "1"}))
        lvl.append(w_el("numFmt", {attr("val"): "bullet"}))
        lvl.append(w_el("lvlText", {attr("val"): "•"}))
        lvl.append(w_el("lvlJc", {attr("val"): "left"}))
        ppr = w_el("pPr")
        ppr.append(w_el("ind", {attr("left"): "720", attr("hanging"): "360"}))
        lvl.append(ppr)
        abstract.append(lvl)
        root.append(abstract)
        num = w_el("num", {attr("numId"): "9"})
        num.append(w_el("abstractNumId", {attr("val"): "9"}))
        root.append(num)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main():
    base = Path.cwd()
    target = base / "NH8.1-VN.BCTK.docx"
    source = base / "NH8.1-VN.BCTK-COMPLETED.docx"
    backup = base / f"NH8.1-VN.BCTK.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.docx"
    tmp = base / "NH8.1-VN.BCTK.updated.tmp.docx"

    shutil.copy2(target, backup)
    document_xml = body_from_source(source, target)

    with zipfile.ZipFile(target, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = document_xml
            elif item.filename == "word/header1.xml":
                data = header_xml()
            elif item.filename == "word/numbering.xml":
                data = update_numbering(data)
            zout.writestr(item, data)

    tmp.replace(target)
    print(f"Updated: {target}")
    print(f"Backup: {backup}")


if __name__ == "__main__":
    main()
