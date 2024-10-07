document.addEventListener('DOMContentLoaded', (event) => {
    const inputs = document.querySelectorAll('.token-input');

    inputs.forEach((input, index) => {
        input.addEventListener('input', (event) => {
            if (event.inputType === 'insertText' && input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });

        input.addEventListener('paste', (event) => {
            event.preventDefault();
            const pasteData = (event.clipboardData || window.clipboardData).getData('text');
            const digits = pasteData.split('').filter(char => /[a-zA-Z0-9]/.test(char));
            for (let i = 0; i < digits.length && i + index < inputs.length; i++) {
                inputs[i + index].value = digits[i];
            }
            if (index + digits.length < inputs.length) {
                inputs[index + digits.length].focus();
            } else {
                inputs[inputs.length - 1].focus();
            }
        });
    });

    const form = document.getElementById('token-form');
    form.addEventListener('submit', (event) => {
        let token = '';
        inputs.forEach(input => {
            token += input.value;
        });
        const hiddenTokenInput = document.createElement('input');
        hiddenTokenInput.type = 'hidden';
        hiddenTokenInput.name = 'token';
        hiddenTokenInput.value = token;
        form.appendChild(hiddenTokenInput);
    });
});