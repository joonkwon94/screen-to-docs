function doPost(e) {
  try {
    // 파이썬 프로그램에서 보낸 JSON 데이터 파싱
    const data = JSON.parse(e.postData.contents);
    const textToAdd = data.text;
    
    if (!textToAdd) {
       return ContentService.createTextOutput("텍스트가 없습니다.").setMimeType(ContentService.MimeType.TEXT);
    }
    
    // 현재 시간 가져오기
    const now = new Date();
    const timeString = now.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
    const docTitle = "스크린 캡처 요약 - " + timeString;
    
    // 구글 드라이브에 [새로운 문서 자동 생성] !!!
    const doc = DocumentApp.create(docTitle);
    const body = doc.getBody();
    
    // 문서에 내용 작성
    body.appendParagraph('🕒 스크랩 시간: ' + timeString);
    body.appendParagraph('--------------------------------------------------');
    body.appendParagraph(textToAdd);
    
    doc.saveAndClose();
    
    // 성공 시 문서 URL 반환
    return ContentService.createTextOutput("Success: " + doc.getUrl()).setMimeType(ContentService.MimeType.TEXT);
    
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
