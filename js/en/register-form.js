/* ---------------------------------------------
Register form
 --------------------------------------------- */
 $(document).ready(function(){

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
    $("#register_form").submit(function (event) {
        event.preventDefault(); // 기본 폼 제출 방지
        
        // 필수 입력 필드 검사
        let isValid = true;
        const requiredFields = {
            'name': 'Name',
            'email': 'Email',
            'company': 'Company',
            'phone-number': 'Phone'
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
            $('#contact_policy_error').text('*Please agree to the collection and use of personal information.');
            isValid = false;
        } else {
            $('#contact_policy_error').text('');
        }

        if (!isValid) {
            return false;
        }

        // 제출 버튼 비활성화 및 로딩 상태 표시
        const submitBtn = $('#submit_btn');
        const originalText = submitBtn.find('span').text();
        submitBtn.prop('disabled', true);
        submitBtn.find('span').text('Sending...');

        // AJAX로 폼 데이터 전송
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
                // 성공 시 alert 메시지
                alert('✅ Your request has been sent successfully!\nWe will follow up at the email address you provided.');
                resetForm();
            },
            error: function(xhr, status, error) {
                // 실패 시 alert 메시지
                alert('❌ An error occurred while sending.\nPlease try again in a moment.');
                console.error('Form submission error:', error);
            },
            complete: function() {
                // 제출 버튼 원상복구
                submitBtn.prop('disabled', false);
                submitBtn.find('span').text(originalText);
            }
        });

    });

    // 입력 필드 변경 시 테두리 색상 초기화
    $("#register_form input, #register_form textarea").on("input", function () {
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
        $("#register_form")[0].reset();
        $("#register_form input, #register_form textarea").css("border-color", "");
        $("#contact_form_container").fadeOut();
        $("#result").slideUp();
        $('#contact_policy_error').text('');
    }
});