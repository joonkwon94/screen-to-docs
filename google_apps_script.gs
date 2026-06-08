function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const textToAdd = data.text;
    const sessionId = data.session_id; 
    const action = data.action || "append"; // 기본값은 내용 추가
    
    const props = PropertiesService.getScriptProperties();
    let docId = props.getProperty(sessionId);
    let doc;
    
    // 세션 종료 요청이 온 경우
    if (action === "finish") {
      if (docId) {
        doc = DocumentApp.openById(docId);
        const body = doc.getBody();
        body.appendParagraph('\n==================================================');
        body.appendParagraph('✅ 모든 스크린샷 캡처 작업이 완료되었습니다. (기록 종료)');
        body.appendParagraph('==================================================\n');
        doc.saveAndClose();
        
        // 세션 아이디 삭제 (더 이상 이 문서에 추가되지 않도록 잠금)
        props.deleteProperty(sessionId);
        return ContentService.createTextOutput("Session Finished").setMimeType(ContentService.MimeType.TEXT);
      }
      return ContentService.createTextOutput("No active session").setMimeType(ContentService.MimeType.TEXT);
    }
    
    // 일반적인 캡처(append) 요청인 경우
    if (!textToAdd) {
       return ContentService.createTextOutput("텍스트가 없습니다.").setMimeType(ContentService.MimeType.TEXT);
    }
    
    if (docId) {
      try {
        doc = DocumentApp.openById(docId);
      } catch(err) {
        docId = null;
      }
    }
    
    if (!docId) {
      const now = new Date();
      const timeString = now.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
      const docTitle = "스크린 캡처 작업물 - " + timeString;
      
      doc = DocumentApp.create(docTitle);
      props.setProperty(sessionId, doc.getId()); 
    }
    
    const body = doc.getBody();
    
    body.appendParagraph(textToAdd);
    body.appendParagraph('--------------------------------------------------\n');
    
    doc.saveAndClose();
    
    return ContentService.createTextOutput("Success: " + doc.getUrl()).setMimeType(ContentService.MimeType.TEXT);
    
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
