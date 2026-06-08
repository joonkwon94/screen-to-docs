// 1. Google 문서(Docs)를 하나 새로 생성합니다.
// 2. 해당 문서의 URL에서 /d/ 와 /edit 사이의 긴 문자열(문서 ID)을 복사합니다.
// 3. 아래 코드의 DOCUMENT_ID 값에 붙여넣습니다.
const DOCUMENT_ID = '여기에_복사한_문서_ID를_넣으세요';

function doPost(e) {
  try {
    // 파이썬 프로그램에서 보낸 JSON 데이터 파싱
    const data = JSON.parse(e.postData.contents);
    const textToAdd = data.text;
    
    if (!textToAdd) {
       return ContentService.createTextOutput("텍스트가 없습니다.").setMimeType(ContentService.MimeType.TEXT);
    }
    
    // 문서 열기 및 텍스트 추가
    const doc = DocumentApp.openById(DOCUMENT_ID);
    const body = doc.getBody();
    
    // 구분선과 시간 추가
    const now = new Date();
    const timeString = now.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
    
    body.appendParagraph('--------------------------------------------------');
    body.appendParagraph(`🕒 스크랩 시간: ${timeString}`);
    
    // 메인 텍스트 추가
    body.appendParagraph(textToAdd);
    body.appendParagraph('\n');
    
    doc.saveAndClose();
    
    return ContentService.createTextOutput("Success").setMimeType(ContentService.MimeType.TEXT);
    
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
