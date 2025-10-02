        function togglePassword(fieldId) {
            const field = document.getElementById(fieldId);
            const btn = field.nextElementSibling;
            
            if (field.type === 'password') {
                field.type = 'text';
                btn.textContent = 'Hide';
            } else {
                field.type = 'password';
                btn.textContent = 'Show';
            }
        }

        function validateEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }

        function validatePhone(phone) {
            return /^[\d\s\-\+\(\)]+$/.test(phone) && phone.replace(/\D/g, '').length >= 10;
        }

        document.getElementById('registerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isValid = true;
            const errors = document.querySelectorAll('.error');
            errors.forEach(err => err.style.display = 'none');

            const fullName = document.getElementById('fullName').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const terms = document.getElementById('terms').checked;

            if (fullName.length < 2) {
                document.getElementById('nameError').style.display = 'block';
                isValid = false;
            }

            if (!validateEmail(email)) {
                document.getElementById('emailError').style.display = 'block';
                isValid = false;
            }

            if (!validatePhone(phone)) {
                document.getElementById('phoneError').style.display = 'block';
                isValid = false;
            }

            if (password.length < 8) {
                document.getElementById('passwordError').style.display = 'block';
                isValid = false;
            }

            if (password !== confirmPassword) {
                document.getElementById('confirmError').style.display = 'block';
                isValid = false;
            }

            if (!terms) {
                alert('Please accept the Terms & Conditions');
                isValid = false;
            }

            if (isValid) {
                const formData = {
                    fullName,
                    email,
                    phone,
                    userType: document.getElementById('userType').value,
                    password
                };

                console.log('Registration data:', formData);
                
                document.getElementById('successMessage').style.display = 'block';
                document.getElementById('registerForm').reset();
                
                setTimeout(() => {
                    alert('Registration successful! In a real application, you would be redirected to the login page.');
                }, 1500);
            }
        });

        function socialLogin(provider) {
            alert(`${provider.charAt(0).toUpperCase() + provider.slice(1)} login would be implemented here`);
        }
