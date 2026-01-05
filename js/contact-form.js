/* ---------------------------------------------
 Contact form
 --------------------------------------------- */
 $(document).ready(function(){
    // Contact Us 버튼 & 폼 토글 기능
    $("#contact_btn").click(function () {
        $("#contact_form_container").fadeIn();
        $(this).hide();
    });

    // X 버튼 클릭 시 폼 숨기고 초기화
    $("#close_btn").click(function () {
        resetForm();
    });

    // 모달 관련 이벤트
    $('#contact_form_modal_open').on('click', function() {
        $('#contact_form_policy_modal').removeClass('blind');
    });

    $('#contact_form_modal_close, #contact_form_modal_bg').on('click', function() {
        $('#contact_form_policy_modal').addClass('blind');
    });

    // submit 버튼 클릭 이벤트
    $("#contact_form").submit(function (event) {
        
        // 필수 입력 필드 검사
        let isValid = true;
        const requiredFields = {
            'name': '이름',
            'email': '이메일',
            'company': '회사',
            'message': '문의내용'
        };

        // 입력 필드 검증
        for (const [field, label] of Object.entries(requiredFields)) {
            const value = $(`input[name=${field}], textarea[name=${field}]`).val().trim();
            if (!value) {
                $(`input[name=${field}], textarea[name=${field}]`).css('border-color', '#e41919');
                isValid = false;
            }
        }

        // 개인정보 동의 체크 여부 확인
        if (!$('#contact_policy').prop('checked')) {
            $('#contact_policy_error').text('*개인정보 수집 및 이용에 동의해주세요.');
            isValid = false;
        } else {
            $('#contact_policy_error').text('');
        }

        if (!isValid) {
            event.preventDefault(); // 폼 제출 방지
            return false;
        }

        // 유효한 경우에는 제출 후 숨기기 (submit 이후 실행됨)
        setTimeout(() => {
            resetForm();
        }, 500);

    });

    // 입력 필드 변경 시 테두리 색상 초기화
    $("#contact_form input, #contact_form textarea").on("input", function () {
        $(this).css("border-color", "");
        $("#result").slideUp();
    });

    // 체크박스 변경 시 에러 메시지 초기화
    $("#contact_policy").change(function() {
        if ($(this).prop('checked')) {
            $('#contact_policy_error').text('');
        }
    });

    // 폼 초기화 함수
    function resetForm() {
        $("#contact_form")[0].reset();
        $("#contact_form input, #contact_form textarea").css("border-color", "");
        $("#contact_form_container").fadeOut();
        $("#contact_btn").fadeIn();
        $("#result").slideUp();
        $('#contact_policy_error').text('');
    }
});