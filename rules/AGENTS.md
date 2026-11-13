# Global Workspace Rules & Intent Classifier

> Áp dụng toàn cục cho mọi dự án, hỗ trợ tự nhiên tiếng Việt và tiếng Anh.

## 1. Nguyên tắc nhận diện ngôn ngữ tiếng Việt tự nhiên
- Luôn thấu hiểu mọi yêu cầu bằng tiếng Việt (bao gồm khẩu ngữ, từ lóng kỹ thuật, cách diễn đạt đời thường).
- Không yêu cầu người dùng phải gõ đúng tên skill hay cú pháp tiếng Anh.
- Tự động map ý định người dùng tới các bộ skills tương ứng:
  * "quy trình trọn gói / end to end / làm từ a tới z / kết hợp spec kit và egm / speckit-egm / egm-speckit / fullcycle / hoàn thiện chuẩn / orchestration spec và phản biện" -> egm-speckit
  * "viết code sạch / gọn lại / dễ đọc" -> clean-code
  * "thiết kế bảng / database / csdl" -> database-design
  * "giao diện đẹp / làm lại ui / bảng màu" -> ui-ux-pro-max
  * "vẽ biểu đồ / làm chart / dashboard" -> lieflat-charts
  * "làm cho nó người hơn / khử giọng ai / nhân tính hơn" -> humanizer
  * "tạo file word / xuất word" -> docx
  * "làm slide / thuyết trình" -> pptx
  * "tính toán / xuất excel" -> xlsx
  * "soi lỗi pr / review pr" -> bmad-os-review-pr
  * "bị lỗi / tìm nguyên nhân / tại sao bị vậy" -> problem-solving-pro
  * "phân vân / nên chọn cái nào / so sánh" -> make-decision
  * "lập spec / viết đặc tả / tạo đề xuất thay đổi" -> openspec-propose
  * "thảo luận ý tưởng / khảo sát giải pháp" -> openspec-explore
  * "triển khai spec / code theo spec" -> openspec-apply-change
  * "nghiệm thu spec / kiểm tra khớp spec" -> openspec-verify-change
  * "lưu trữ spec / đóng spec" -> openspec-archive-change
  * "lên spec chuẩn / spec kit / đặc tả yêu cầu / spec-driven" -> speckit-specify / speckit
  * "lên plan kỹ thuật / lập kế hoạch kiến trúc / technical plan" -> speckit-plan
  * "chia task theo spec / lập checklist công việc / task breakdown" -> speckit-tasks
  * "thực thi code theo spec / implement spec" -> speckit-implement
  * "làm rõ spec / loại bỏ giả định mù / clarify spec" -> speckit-clarify
  * "kiểm tra nhất quán spec / analyze spec / audit spec" -> speckit-analyze
  * "nguyên tắc kiến trúc dự án / hiến chương dự án / constitution" -> speckit-constitution
  * "đối soát hoàn thiện code theo spec / converge spec" -> speckit-converge
  * "kiểm tra tiêu chí nghiệm thu / quality checklist" -> speckit-checklist
  * "nghiên cứu suy luận / phản biện độc lập / goldfish review / elephant brainstorm / egm" -> egm-review / egm-brainstorm / egm-review-loop
  * "phản biện thiết kế / soi lỗ hổng giả định / review độc lập / subagent phản biện" -> egm-review
  * "brainstorm giải pháp / mở rộng ý tưởng với context / tư duy phân kỳ" -> egm-brainstorm
  * "soạn thảo tài liệu thiết kế / draft spec kiến trúc / viết design doc" -> egm-draft
  * "giải quyết phản biện / chốt phương án sau review / resolve review" -> egm-resolve
  * "khảo sát codebase / bootstrap context dự án / hiểu mã nguồn sâu" -> egm-bootstrap
  * "đánh giá lệch chuẩn code và spec / drift report / kiểm tra sai lệch spec" -> egm-drift-report
  * "nghiên cứu khoa học / ý tưởng nghiên cứu / brainstorm đề tài" -> scientific-brainstorming
  * "phản biện khoa học / đánh giá bằng chứng / tư duy phản biện" -> scientific-critical-thinking
  * "viết bài báo khoa học / viết paper / bản thảo nghiên cứu" -> scientific-writing
  * "tổng quan tài liệu / tìm paper / tổng thuật y sinh" -> literature-review
  * "thiết kế thí nghiệm / phương pháp nghiên cứu" -> experimental-design
  * "phân tích thống kê khoa học / kiểm định số liệu" -> statistical-analysis
  * "thuật toán mạng xã hội / content từng nền tảng / viral threads" -> platform-content-strategy
  * "trau chuốt ui / làm đẹp giao diện đỉnh cao / thiết kế đẳng cấp / audit ui" -> impeccable
  * "chống slop / thẩm mỹ giao diện / gu thiết kế / landing page đẹp" -> design-taste-frontend
  * "giao diện tối giản / phong cách báo chí / minimalist" -> minimalist-ui
  * "giao diện brutalist / thô mộc / phong cách kỹ thuật" -> industrial-brutalist-ui
  * "viết code đầy đủ / không viết tắt / không bỏ sót code" -> full-output-enforcement
  * "review code đa ngôn ngữ / kiểm tra pr chi tiết" -> code-review-skill
  * "founder review / góc nhìn ceo / đánh giá ý tưởng lớn" -> plan-ceo-review
  * "eng manager review / đánh giá kiến trúc kỹ thuật" -> plan-eng-review
  * "tìm bug / test giao diện / qa hệ thống" -> qa
  * "ship code / ra mắt tính năng / đóng gói release" -> ship
  * "bàn giao phiên bản / handoff công việc" -> handoff
  * "nén context / quản lý ngữ cảnh chủ động" -> strategic-compact

## 2. Tiêu chuẩn phản hồi & Hoạt động Subagent
- Giữ phong cách ngắn gọn, súc tích, giải quyết thẳng vào vấn đề.
- Ưu tiên hiển thị giải pháp hoặc code mẫu trực tiếp, không vòng vo giải thích thừa.
- Khi thực thi **egm-speckit / speckit-egm (Full-Cycle Orchestrator)**: Chạy liên tục từ Stage 1 (Spec Kit: Specification & Clarify) $\rightarrow$ Stage 2 (EGM Swarm Review: `invoke_subagent` cho `egm-design`, `egm-zoom-out`, `egm-codebase-details`, `egm-synthesizer`) $\rightarrow$ Stage 3 (Plan & Tasks: `speckit-plan`, `egm-implementation-readiness`, `speckit-tasks`, `speckit-analyze`) $\rightarrow$ Stage 4 (Implement & Converge: `speckit-implement`, testing, `speckit-converge`).
- Khi thực thi **EGM Goldfish Review**: Subagent review BẮT BUỘC chạy trong ngữ cảnh độc lập mới (`invoke_subagent` với prompt persona từ `agents/<persona>.md`), không bị bias bởi hội thoại cha, đối chiếu trực tiếp với tài liệu thiết kế và tiêu chuẩn tài liệu `resources/document_standards/`.
- Khi thực thi **Spec Kit (SDD)**: Luôn đi theo quy trình chặt chẽ: `Constitution` -> `Specify` -> `Clarify` -> `Plan` -> `Tasks` -> `Implement` -> `Converge`. Nếu dự án chưa có `.specify/`, chạy `specify init --here --force --integration agy --non-interactive --script ps` hoặc dùng bộ template/script được đóng gói sẵn.
