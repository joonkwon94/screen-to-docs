function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const textToAdd = data.text;
    const sessionId = data.session_id; // 파이썬이 실행될 때마다 고유한 세션 ID를 보냅니다.
    
    if (!textToAdd) {
       return ContentService.createTextOutput("텍스트가 없습니다.").setMimeType(ContentService.MimeType.TEXT);
    }
    
    const props = PropertiesService.getScriptProperties();
    let docId = props.getProperty(sessionId);
    let doc;
    
    // 이 세션(현재 파이썬 실행)에서 이미 만들어진 문서가 있다면 그걸 엽니다.
    if (docId) {
      try {
        doc = DocumentApp.openById(docId);
      } catch(err) {
        // 에러가 나면 새로 만듭니다.
        docId = null;
      }
    }
    
    // 아직 만들어진 문서가 없다면 새 문서를 생성합니다.
    if (!docId) {
      const now = new Date();
      const timeString = now.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
      const docTitle = "스크린 캡처 작업물 - " + timeString;
      
      doc = DocumentApp.create(docTitle);
      props.setProperty(sessionId, doc.getId()); // 이번 세션 ID에 생성된 문서 ID를 기억해둡니다.
    }
    
    const body = doc.getBody();
    const currentTime = new Date().toLocaleTimeString('ko-KR', { timeZone: 'Asia/Seoul' });
    
    // 내용 추가
    body.appendParagraph('🕒 캡처 시간: ' + currentTime);
    body.appendParagraph(textToAdd);
    body.appendParagraph('--------------------------------------------------\n');
    
    doc.saveAndClose();
    
    return ContentService.createTextOutput("Success: " + doc.getUrl()).setMimeType(ContentService.MimeType.TEXT);
    
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
