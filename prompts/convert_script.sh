#!/bin/bash

# This script will be used to systematically track the conversions
# We'll do the actual conversions using Claude Code's Write tool

echo "Teaching Assistant File Conversion Script"
echo "=========================================="
echo ""
echo "Files to convert:"
echo "1. ティーチングアシスト_直接指導型.md → TeachingAssistant_DirectInstruction_Japanese.md"
echo "2. ティーチングアシスト_思考促進型.md → TeachingAssistant_ThinkingPromotion_Japanese.md"
echo "3. ティーチングアシスト_初学者向け.md → TeachingAssistant_Beginner_Japanese.md"
echo "4. ティーチングアシスト_試験対策.md → TeachingAssistant_ExamPrep_Japanese.md"
echo "5. ティーチングアシスト_研究入門.md → TeachingAssistant_ResearchIntro_Japanese.md"
echo "6. ティーチングアシスト_オンライン授業専門.md → TeachingAssistant_OnlineClass_Japanese.md"
echo "7. ティーチングアシスト_高校数学_直接指導型.md → TeachingAssistant_HighSchoolMath_Direct_Japanese.md"
echo "8. ティーチングアシスト_高校数学_思考促進型.md → TeachingAssistant_HighSchoolMath_Thinking_Japanese.md"
echo "9. ティーチングアシスト_高校情報_指導.md → TeachingAssistant_HighSchoolCS_Direct_Japanese.md"
echo "10. ティーチングアシスト_高校情報_探求.md → TeachingAssistant_HighSchoolCS_Inquiry_Japanese.md"
echo "11. ティーチングアシスト_プログラミング演習_指導.md → TeachingAssistant_Programming_Direct_Japanese.md"
echo "12. ティーチングアシスト_プログラミング演習_探求.md → TeachingAssistant_Programming_Inquiry_Japanese.md"
echo "13. ティーチングアシスト_データサイエンス_直接指導型.md → TeachingAssistant_DataScience_Direct_Japanese.md"
echo "14. ティーチングアシスト_データサイエンス_探求型.md → TeachingAssistant_DataScience_Inquiry_Japanese.md"
echo "15. 多様な視点の同級生.md → DiversePeerPerspectives_Japanese.md"
echo "16. 高校生探求学習ファシリテーター.md → HighSchoolInquiryFacilitator_Japanese.md"
