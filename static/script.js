// 불러오기
const imageUpload = document.getElementById("image-upload");
const uploadButton = document.getElementById("upload-button");
const resetButton = document.getElementById("reset-button");
const inferenceButton = document.getElementById("inference-button")

const originalImage = document.getElementById("original-image");
const inferenceText = document.getElementById("inference_text")
const inferenceNum = document.getElementById("inference_num")

// 리셋 함수
function resetImage() {
    // 이미지 업로드 입력 필드 초기화
    imageUpload.value = null;

    // 결과 이미지 숨김
    originalImage.style.display = "none";
    inferenceText.style.display = "none";
    inferenceNum.style.display = "none";

    // 이미지 초기화 (선택한 이미지 제거)
    originalImage.src = "";

    // 서버에 이미지 초기화 요청 보내기
    fetch("/reset/", {
        method: "POST"
    })
    .then(response => response.json())
    .catch(error => {
        console.error("Error:", error);
    });
}

// 이미지 초기화 버튼 클릭 이벤트 처리
resetButton.addEventListener("click", () => {
    resetImage();
});


// 이미지 선택 이벤트 처리
document.getElementById("image-upload").addEventListener("change", () => {
    const file = document.getElementById("image-upload").files[0];

    if (file) {
        // 파일이 선택되면 업로드 진행
        uploadImage(file);
    }
});

// 업로드 함수
function uploadImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    // 서버로 이미지 업로드 요청
    fetch("/upload/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const filename = data.filename;
        
        // 랜덤한 쿼리 매개변수를 이미지 URL에 추가하여 캐싱 방지
        const randomQuery = new Date().getTime();
        const imageUrl = `/uploads/${filename}?${randomQuery}`;

        // 이미지 URL 업데이트
        originalImage.src = imageUrl;

        // 결과 섹션 표시
        originalImage.style.display = "block";
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// 업로드 버튼 클릭 이벤트 처리
uploadButton.addEventListener("click", () => {
    // 이미지 초기화
    resetButton.click();

    // 파일 선택 창 열기
    imageUpload.click();
});

// 페이지 로드 시 초기화
window.addEventListener("load", () => {
    // 이미지 초기화
    resetButton.click();
});

// 추론 함수
function displayInferenceResult() {
    // 추론 엔드포인트로 POST 요청 보내기
    fetch("/inference/", {
        method: "POST",
        body: JSON.stringify({}),
        headers: {
            "Content-Type": "application/json", 
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.predt) {
            // 'inference' 엘리먼트에 예측 결과를 설정
            inferenceText.textContent = `${data.predt}`;
            inferenceNum.textContent = `${data.predn}`;
        } else if (data.error) {
            inferenceText.textContent = `오류: ${data.error}`;
        }
        inferenceText.style.display = "block";
        inferenceNum.style.display = "block";
    })
    .catch(error => {
        console.error("오류:", error);
    });
}

// 추론 버튼 클릭 시 이벤트 처리
inferenceButton.addEventListener("click", () => {
    // 추론
    displayInferenceResult();
});

