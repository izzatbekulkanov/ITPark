// JavaScript funksiyasi
            function populateServiceTable(services) {
                // HTML jadvalidagi tbody elementini tanlash
                var tbody = document.querySelector('.js-table-sections tbody.js-table-sections-header');

                // Eski ma'lumotlarni tozalash
                tbody.innerHTML = '';

                // Har bir xizmat uchun ma'lumotlar ro'yxatini yaratish va jadvalga qo'shish
                services.services.forEach(function (service) {
                    // Service.created_at ni JavaScript Date obyektiga o'tkazish
                    var createdAt = new Date(service.created_at);

                    // JavaScript Date obyektini yil, oy, kun ko'rinishida formatlash
                    var dateString = createdAt.toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });

                    // Yangi qator elementini yaratish
                    var row = document.createElement('tr');

                    // Qator elementiga ma'lumotlar qo'shish
                    row.innerHTML = `
                    <td class="fw-semibold">${service.name}</td>
                    <td>
                        <span class="badge bg-success">${service.code}</span>
                    </td>
                    <td class="d-none d-sm-table-cell">
                        ${dateString}
                    </td>
                `;

                    // Yangi qator elementini tbody ga qo'shish
                    tbody.appendChild(row);
                });
            }

            // Service lar ro'yxatini olish uchun AJAX so'rov
            function fetchServices() {
                // AJAX so'rov yuborish
                fetch('/json/get_service_list')
                    .then(response => response.json())
                    .then(data => {
                        // Qayta yuklash funksiyasini chaqirish
                        populateServiceTable(data);
                    })
                    .catch(error => console.error('Error fetching services:', error));
            }

            $(document).ready(function () {
                $("#saveServiceBtns").click(function () {
                    var serviceName = $("#serviceName").val();
                    var serviceCode = $("#serviceCode").val();
                    var serviceIcon = $("#serviceIcon").val();

                    $.ajax({
                        type: "POST",
                        url: "/json/create_service",
                        data: {
                            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                            'name': serviceName,
                            'code': serviceCode,
                            'icon': serviceIcon
                        },
                        success: function (response) {
                            // Ma'lumotlar muvaffaqiyatli saqlangan bo'lsa, modalni yopib va formadagi ma'lumotlarni tozalash
                            $('#modal-small').modal('hide');  // Modalni yopish
                            $("#serviceName").val('');  // Formadagi ma'lumotlarni tozalash
                            $("#serviceCode").val('');
                            $("#serviceIcon").val('');
                            fetchServices();  // Xizmatlar ro'yxatini qayta yuklash
                        },
                        error: function (xhr, errmsg, err) {
                            console.log(xhr.status + ": " + xhr.responseText);
                            alert("Xato! Xizmat qo'shilmadi.");
                        }
                    });
                });

                // Boshlang'ich yuklashda `fetchServices()` funksiyasini chaqirish
                fetchServices();
            });