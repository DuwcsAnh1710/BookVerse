# Checkout JavaScript logic for DuwcsAnhLib - MoMo & COD
CHECKOUT_JS = """
    // === FLATSOME WOOCOMMERCE CHECKOUT CONTROLLERS ===
    let currentPaymentMethod = 'bacs'; // MoMo is default
    let checkoutVoucherDiscount = 0;
    let checkoutAppliedVoucher = '';
    let lastGeneratedOrder = null;

    function selectPaymentMethod(method) {
      currentPaymentMethod = method;
      const bacsBox = document.getElementById('payOptionBACS');
      const codBox = document.getElementById('payOptionCOD');
      const bacsDetails = document.getElementById('bacsDetailsBox');
      const codDetails = document.getElementById('codDetailsBox');
      const radioBACS = document.getElementById('radioPayBACS');
      const radioCOD = document.getElementById('radioPayCOD');

      if (method === 'bacs') {
        if (radioBACS) radioBACS.checked = true;
        if (bacsBox) {
          bacsBox.className = 'border-2 border-[#A50064] bg-[#A50064]/5 rounded-xl p-3.5 sm:p-4 cursor-pointer transition';
        }
        if (codBox) {
          codBox.className = 'border border-gray-200 bg-white hover:border-gray-300 rounded-xl p-3.5 sm:p-4 cursor-pointer transition';
        }
        if (bacsDetails) bacsDetails.classList.remove('hidden');
        if (codDetails) codDetails.classList.add('hidden');
      } else {
        if (radioCOD) radioCOD.checked = true;
        if (codBox) {
          codBox.className = 'border-2 border-brand-red bg-red-50/40 rounded-xl p-3.5 sm:p-4 cursor-pointer transition';
        }
        if (bacsBox) {
          bacsBox.className = 'border border-gray-200 bg-white hover:border-gray-300 rounded-xl p-3.5 sm:p-4 cursor-pointer transition';
        }
        if (codDetails) codDetails.classList.remove('hidden');
        if (bacsDetails) bacsDetails.classList.add('hidden');
      }
    }

    function renderCheckoutPage() {
      const emptyState = document.getElementById('checkoutEmptyState');
      const formGrid = document.getElementById('checkoutFormGrid');
      const itemsContainer = document.getElementById('checkoutCartItems');
      const countBadge = document.getElementById('checkoutItemCountBadge');
      
      if (!emptyState || !formGrid) return;

      const totalQty = cart.reduce((acc, x) => acc + x.qty, 0);
      if (countBadge) countBadge.textContent = totalQty + ' cuốn';

      if (cart.length === 0) {
        emptyState.classList.remove('hidden');
        formGrid.classList.add('hidden');
        return;
      }

      emptyState.classList.add('hidden');
      formGrid.classList.remove('hidden');

      // Populate Items List
      if (itemsContainer) {
        itemsContainer.innerHTML = cart.map(item => {
          const p = allProducts.find(x => x.SKU === item.sku);
          const cover = p ? `assets/covers/${item.sku}.png` : 'assets/logo-header-symbol.png';
          return `
            <div class="flex items-center gap-3 py-2.5">
              <img src="${cover}" alt="${item.name}" class="w-11 h-15 object-cover rounded shadow-sm shrink-0 border border-gray-200">
              <div class="flex-1 min-w-0">
                <h4 class="font-bold text-xs text-gray-900 truncate" title="${item.name}">${item.name}</h4>
                <div class="flex items-center gap-2 text-[11px] text-gray-500 mt-0.5">
                  <span class="bg-gray-100 px-1.5 py-0.5 rounded font-mono font-bold text-gray-700">SL: ${item.qty}</span>
                  <span>×</span>
                  <span>${formatVND(item.price)}</span>
                </div>
              </div>
              <div class="text-right shrink-0">
                <span class="font-bold text-xs text-brand-red">${formatVND(item.price * item.qty)}</span>
              </div>
            </div>
          `;
        }).join('');
      }

      // Calculations
      const subtotal = cart.reduce((acc, x) => acc + (x.price * x.qty), 0);
      const freeThreshold = 250000;
      let shipping = subtotal >= freeThreshold ? 0 : 25000;

      // Calculate voucher discount
      let discount = 0;
      if (checkoutAppliedVoucher === 'DUWCSANH10') {
        discount = Math.round(subtotal * 0.1);
      } else if (checkoutAppliedVoucher === 'TRIAN') {
        discount = Math.min(subtotal, 20000);
      }
      checkoutVoucherDiscount = discount;

      const finalTotal = Math.max(0, subtotal - discount + shipping);

      // Update Displays
      const subEl = document.getElementById('checkoutSubtotalDisplay');
      const discEl = document.getElementById('checkoutDiscountDisplay');
      const shipEl = document.getElementById('checkoutShippingDisplay');
      const totEl = document.getElementById('checkoutTotalDisplay');
      const freeshipTag = document.getElementById('checkoutFreeshipTag');
      const freeshipMsg = document.getElementById('checkoutFreeshipMsg');

      if (subEl) subEl.textContent = formatVND(subtotal);
      if (discEl) discEl.textContent = discount > 0 ? ('-' + formatVND(discount)) : '0 đ';
      if (shipEl) shipEl.textContent = shipping === 0 ? 'Miễn phí (FREESHIP)' : formatVND(shipping);
      if (totEl) totEl.textContent = formatVND(finalTotal);

      if (freeshipTag && freeshipMsg) {
        if (subtotal >= freeThreshold) {
          freeshipTag.className = 'text-[11px] text-emerald-800 bg-emerald-50 px-2.5 py-1.5 rounded-lg border border-emerald-200 flex items-center gap-1.5 font-bold';
          freeshipMsg.textContent = 'Đơn hàng đạt chuẩn Miễn Phí Vận Chuyển toàn quốc!';
        } else {
          const remain = freeThreshold - subtotal;
          freeshipTag.className = 'text-[11px] text-amber-800 bg-amber-50 px-2.5 py-1.5 rounded-lg border border-amber-200 flex items-center gap-1.5 font-medium';
          freeshipMsg.textContent = `Mua thêm ${formatVND(remain)} để được FREESHIP 0đ`;
        }
      }
    }

    function setCheckoutVoucher(code) {
      const inp = document.getElementById('checkoutVoucherInput');
      if (inp) inp.value = code;
      applyCheckoutVoucher();
    }

    function applyCheckoutVoucher() {
      const inp = document.getElementById('checkoutVoucherInput');
      const code = (inp ? inp.value : '').trim().toUpperCase();
      
      if (!code) {
        checkoutAppliedVoucher = '';
        renderCheckoutPage();
        return;
      }

      if (code === 'DUWCSANH10') {
        checkoutAppliedVoucher = 'DUWCSANH10';
        showToast('Áp dụng thành công mã <strong>DUWCSANH10</strong> (Giảm 10%)!');
      } else if (code === 'TRIAN') {
        checkoutAppliedVoucher = 'TRIAN';
        showToast('Áp dụng thành công mã <strong>TRIAN</strong> (Giảm 20.000 đ)!');
      } else {
        alert('Mã giảm giá không hợp lệ hoặc đã hết hạn! Vui lòng thử DUWCSANH10 hoặc TRIAN.');
        checkoutAppliedVoucher = '';
      }
      renderCheckoutPage();
    }

    function processFullCheckout() {
      if (cart.length === 0) {
        alert('Giỏ hàng của bạn đang trống! Vui lòng chọn sách trước khi đặt hàng.');
        showView('shop');
        return;
      }

      const name = (document.getElementById('checkoutCustName')?.value || '').trim();
      const phone = (document.getElementById('checkoutCustPhone')?.value || '').trim();
      const email = (document.getElementById('checkoutCustEmail')?.value || '').trim();
      const city = document.getElementById('checkoutCustCity')?.value || 'Hồ Chí Minh';
      const address = (document.getElementById('checkoutCustAddress')?.value || '').trim();
      const note = (document.getElementById('checkoutCustNote')?.value || '').trim();

      if (!name) {
        alert('Vui lòng nhập Họ và tên người nhận hàng!');
        document.getElementById('checkoutCustName')?.focus();
        return;
      }
      if (!phone || phone.length < 9) {
        alert('Vui lòng nhập Số điện thoại hợp lệ để giao hàng!');
        document.getElementById('checkoutCustPhone')?.focus();
        return;
      }
      if (!address) {
        alert('Vui lòng nhập Địa chỉ chi tiết để bưu tá giao sách!');
        document.getElementById('checkoutCustAddress')?.focus();
        return;
      }

      // Calculations
      const subtotal = cart.reduce((acc, x) => acc + (x.price * x.qty), 0);
      const shipping = subtotal >= 250000 ? 0 : 25000;
      let discount = 0;
      if (checkoutAppliedVoucher === 'DUWCSANH10') discount = Math.round(subtotal * 0.1);
      else if (checkoutAppliedVoucher === 'TRIAN') discount = Math.min(subtotal, 20000);
      const finalTotal = Math.max(0, subtotal - discount + shipping);

      // Generate Order Code #DAL-XXXX
      const numCode = Math.floor(1000 + Math.random() * 9000);
      const orderCode = 'DAL-' + numCode;
      const cleanOrderCode = 'DAL' + numCode;
      const orderDateStr = new Date().toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });

      // Save order record
      lastGeneratedOrder = {
        code: orderCode,
        cleanCode: cleanOrderCode,
        date: orderDateStr,
        name: name,
        phone: phone,
        email: email,
        city: city,
        address: address,
        note: note,
        method: currentPaymentMethod,
        items: [...cart],
        subtotal: subtotal,
        discount: discount,
        shipping: shipping,
        total: finalTotal
      };

      try {
        const savedOrders = JSON.parse(localStorage.getItem('duwcsanhlib_orders') || '[]');
        savedOrders.unshift(lastGeneratedOrder);
        localStorage.setItem('duwcsanhlib_orders', JSON.stringify(savedOrders.slice(0, 20)));
      } catch(e) {}

      // Populate Success View
      const succCode = document.getElementById('succOrderCode');
      const succDate = document.getElementById('succOrderDate');
      const succTotal = document.getElementById('succOrderTotal');
      const succMethod = document.getElementById('succOrderMethod');
      if (succCode) succCode.textContent = '#' + orderCode;
      if (succDate) succDate.textContent = orderDateStr;
      if (succTotal) succTotal.textContent = formatVND(finalTotal);
      if (succMethod) succMethod.textContent = currentPaymentMethod === 'bacs' ? 'Ví Điện Tử MoMo / MoMo QR' : 'Thanh toán khi nhận sách (COD)';

      // MoMo QR vs COD sections
      const vietQRSection = document.getElementById('succVietQRSection');
      const codSection = document.getElementById('succCODSection');

      if (currentPaymentMethod === 'bacs') {
        if (vietQRSection) vietQRSection.classList.remove('hidden');
        if (codSection) codSection.classList.add('hidden');
        
        // Generate MoMo QR via Napas/VietQR API (MoMo BIN: 971025)
        const qrUrl = `https://api.vietqr.io/image/971025-0933543987-compact2.jpg?amount=${finalTotal}&addInfo=${cleanOrderCode}&accountName=DUWCSANHLIB`;
        const qrImg = document.getElementById('succVietQRImage');
        if (qrImg) qrImg.src = qrUrl;

        const copyAmountEl = document.getElementById('succCopyAmount');
        const copyContentEl = document.getElementById('succCopyContent');
        if (copyAmountEl) copyAmountEl.textContent = formatVND(finalTotal);
        if (copyContentEl) copyContentEl.textContent = cleanOrderCode;

        const btnOpenMoMo = document.getElementById('btnOpenMoMoApp');
        if (btnOpenMoMo) {
          btnOpenMoMo.href = `https://me.momo.vn/0933543987`;
        }
      } else {
        if (vietQRSection) vietQRSection.classList.add('hidden');
        if (codSection) codSection.classList.remove('hidden');
        
        const codPhone = document.getElementById('succCODPhone');
        const codAmount = document.getElementById('succCODAmount');
        if (codPhone) codPhone.textContent = phone;
        if (codAmount) codAmount.textContent = formatVND(finalTotal);
      }

      // Customer Details
      const succName = document.getElementById('succCustName');
      const succPhone = document.getElementById('succCustPhone');
      const succAddress = document.getElementById('succCustAddress');
      const succNote = document.getElementById('succCustNote');
      if (succName) succName.textContent = name;
      if (succPhone) succPhone.textContent = phone;
      if (succAddress) succAddress.textContent = `${address}, ${city}`;
      if (succNote) succNote.textContent = note || 'Không có ghi chú thêm';

      // Table of items
      const tableBody = document.getElementById('succItemsTableBody');
      if (tableBody) {
        tableBody.innerHTML = cart.map(item => `
          <tr class="hover:bg-gray-50/70">
            <td class="py-2.5 px-3 font-semibold text-gray-800">${item.name}</td>
            <td class="py-2.5 px-3 text-center font-bold text-gray-600">${item.qty}</td>
            <td class="py-2.5 px-3 text-right text-gray-500">${formatVND(item.price)}</td>
            <td class="py-2.5 px-3 text-right font-black text-brand-red">${formatVND(item.price * item.qty)}</td>
          </tr>
        `).join('') + `
          <tr class="bg-gray-50 font-bold border-t border-gray-200">
            <td colspan="3" class="py-2 px-3 text-right text-gray-600">Phí vận chuyển:</td>
            <td class="py-2 px-3 text-right text-gray-800">${shipping === 0 ? 'Miễn phí' : formatVND(shipping)}</td>
          </tr>
          ${discount > 0 ? `
          <tr class="bg-gray-50 font-bold">
            <td colspan="3" class="py-2 px-3 text-right text-emerald-600">Giảm giá voucher:</td>
            <td class="py-2 px-3 text-right text-emerald-600">-${formatVND(discount)}</td>
          </tr>
          ` : ''}
          <tr class="bg-red-50 font-black text-brand-red text-xs sm:text-sm">
            <td colspan="3" class="py-2.5 px-3 text-right uppercase">TỔNG THANH TOÁN:</td>
            <td class="py-2.5 px-3 text-right">${formatVND(finalTotal)}</td>
          </tr>
        `;
      }

      // Clear Cart
      cart = [];
      checkoutAppliedVoucher = '';
      updateCartUI();

      // Show Success View
      showView('order-success');
      showToast('Đơn hàng <strong>#' + orderCode + '</strong> đã được đặt thành công!');
    }

    // 1-Click Copy helpers
    function copyText(str, btn) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(str).then(() => {
          showCopySuccess(btn);
        }).catch(() => fallbackCopy(str, btn));
      } else {
        fallbackCopy(str, btn);
      }
    }

    function copyAmount(btn) {
      if (lastGeneratedOrder) {
        copyText(lastGeneratedOrder.total.toString(), btn);
      }
    }

    function copyContent(btn) {
      if (lastGeneratedOrder) {
        copyText(lastGeneratedOrder.cleanCode, btn);
      }
    }

    function fallbackCopy(str, btn) {
      const ta = document.createElement('textarea');
      ta.value = str;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        showCopySuccess(btn);
      } catch(e) {}
      document.body.removeChild(ta);
    }

    function showCopySuccess(btn) {
      if (!btn) return;
      const originalHTML = btn.innerHTML;
      btn.innerHTML = '<span class="material-symbols-outlined text-xs">check</span><span>Đã chép!</span>';
      btn.classList.add('bg-emerald-600', 'text-white');
      setTimeout(() => {
        btn.innerHTML = originalHTML;
        btn.classList.remove('bg-emerald-600', 'text-white');
      }, 2000);
    }
"""

