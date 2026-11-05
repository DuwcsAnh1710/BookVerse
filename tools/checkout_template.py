# Flatsome-inspired WooCommerce Checkout Flow Templates
# DuwcsAnhLib Storefront - MoMo QR & COD Integration

CHECKOUT_VIEW_HTML = """
    <!-- VIEW: CHECKOUT PAGE (FLATSOME / WOOCOMMERCE STYLE) -->
    <div id="view-checkout" class="hidden space-y-6 max-w-6xl mx-auto w-full px-2 sm:px-4">
      
      <!-- Flatsome Breadcrumbs / Step Process Indicator -->
      <div class="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm">
        <div class="flex items-center justify-center gap-2 sm:gap-6 text-[11px] sm:text-xs font-bold uppercase tracking-wider">
          <button onclick="openCart()" class="flex items-center gap-1.5 text-gray-500 hover:text-brand-red transition cursor-pointer">
            <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-gray-100 flex items-center justify-center text-[10px] sm:text-xs font-bold text-gray-600">1</span>
            <span>Giỏ hàng</span>
          </button>
          <span class="material-symbols-outlined text-gray-300 text-sm">chevron_right</span>
          <div class="flex items-center gap-1.5 text-brand-red font-black">
            <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-brand-red text-white flex items-center justify-center text-[10px] sm:text-xs font-bold shadow-sm">2</span>
            <span>Thông tin &amp; Thanh toán</span>
          </div>
          <span class="material-symbols-outlined text-gray-300 text-sm">chevron_right</span>
          <div class="flex items-center gap-1.5 text-gray-400">
            <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-gray-100 flex items-center justify-center text-[10px] sm:text-xs font-bold text-gray-400">3</span>
            <span>Hoàn tất</span>
          </div>
        </div>
      </div>

      <!-- Checkout Container (Empty Cart State vs 2-Column Form) -->
      <div id="checkoutEmptyState" class="hidden bg-white rounded-2xl p-12 border border-gray-200 shadow-sm text-center space-y-4">
        <div class="w-16 h-16 mx-auto rounded-full bg-red-50 text-brand-red flex items-center justify-center">
          <span class="material-symbols-outlined text-3xl">remove_shopping_cart</span>
        </div>
        <h3 class="text-lg font-bold text-gray-900">Giỏ hàng của bạn đang trống!</h3>
        <p class="text-xs text-gray-500 max-w-md mx-auto">Hãy khám phá 25 ấn bản sách tuyển chọn từ DuwcsAnhLib để chọn cho mình những cuốn sách ưng ý nhất.</p>
        <button onclick="showView('shop')" class="px-6 py-2.5 bg-brand-red text-white text-xs font-bold rounded-xl hover:bg-red-700 transition shadow-md cursor-pointer">
          Khám phá cửa hàng ngay
        </button>
      </div>

      <div id="checkoutFormGrid" class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- Left Column: Shipping & Payment (7 Cols) -->
        <div class="lg:col-span-7 space-y-5">
          
          <!-- Section 1: Customer & Delivery Info -->
          <div class="bg-white rounded-2xl p-4 sm:p-6 border border-gray-200 shadow-sm space-y-4">
            <div class="flex items-center gap-2 pb-3 border-b border-gray-100">
              <span class="material-symbols-outlined text-brand-red text-xl">local_shipping</span>
              <h3 class="text-sm sm:text-base font-black text-gray-900 uppercase">1. Thông tin giao hàng &amp; Người nhận</h3>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="sm:col-span-2">
                <label class="block font-bold text-gray-700 mb-1">Họ và tên người nhận <span class="text-brand-red">*</span></label>
                <input type="text" id="checkoutCustName" placeholder="Ví dụ: Nguyễn Văn An" value="Nguyễn Văn An" class="w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-brand-red focus:ring-1 focus:ring-brand-red outline-none text-xs">
              </div>

              <div>
                <label class="block font-bold text-gray-700 mb-1">Số điện thoại <span class="text-brand-red">*</span></label>
                <input type="tel" id="checkoutCustPhone" placeholder="Ví dụ: 0933543987" value="0933543987" class="w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-brand-red focus:ring-1 focus:ring-brand-red outline-none text-xs">
              </div>

              <div>
                <label class="block font-bold text-gray-700 mb-1">Địa chỉ Email (Nhận mã đơn)</label>
                <input type="email" id="checkoutCustEmail" placeholder="email@example.com" value="khachhang@duwcsanhlib.vn" class="w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-brand-red focus:ring-1 focus:ring-brand-red outline-none text-xs">
              </div>

              <div class="sm:col-span-2">
                <label class="block font-bold text-gray-700 mb-1">Tỉnh / Thành phố <span class="text-brand-red">*</span></label>
                <select id="checkoutCustCity" class="w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-brand-red focus:ring-1 focus:ring-brand-red outline-none text-xs cursor-pointer">
                  <option value="Hồ Chí Minh">TP. Hồ Chí Minh (Giao 1-2 ngày)</option>
                  <option value="Hà Nội">Hà Nội (Giao 2-3 ngày)</option>
                  <option value="Đà Nẵng">Đà Nẵng (Giao 2-3 ngày)</option>
                  <option value="Cần Thơ">Cần Thơ (Giao 2-3 ngày)</option>
                  <option value="Hải Phòng">Hải Phòng (Giao 2-3 ngày)</option>
                  <option value="Bình Dương">Bình Dương (Giao 1-2 ngày)</option>
                  <option value="Đồng Nai">Đồng Nai (Giao 1-2 ngày)</option>
                  <option value="Khác">Tỉnh / Thành phố khác</option>
                </select>
              </div>

              <div class="sm:col-span-2">
                <label class="block font-bold text-gray-700 mb-1">Địa chỉ chi tiết (Số nhà, đường, phường/xã) <span class="text-brand-red">*</span></label>
                <input type="text" id="checkoutCustAddress" placeholder="Ví dụ: 123 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1" value="123 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1" class="w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-brand-red focus:ring-1 focus:ring-brand-red outline-none text-xs">
              </div>

              <div class="sm:col-span-2">
                <label class="block font-bold text-gray-700 mb-1">Ghi chú đơn hàng (Tùy chọn)</label>
                <textarea id="checkoutCustNote" rows="2" placeholder="Giao giờ hành chính, gọi trước khi giao, đóng gói cẩn thận..." class="w-full px-3.5 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-brand-red focus:ring-1 focus:ring-brand-red outline-none text-xs resize-none"></textarea>
              </div>
            </div>
          </div>

          <!-- Section 2: Flatsome Payment Methods Accordion -->
          <div class="bg-white rounded-2xl p-4 sm:p-6 border border-gray-200 shadow-sm space-y-4">
            <div class="flex items-center gap-2 pb-3 border-b border-gray-100">
              <span class="material-symbols-outlined text-brand-red text-xl">payments</span>
              <h3 class="text-sm sm:text-base font-black text-gray-900 uppercase">2. Phương thức thanh toán</h3>
            </div>

            <!-- Payment Options Radio Accordion -->
            <div class="space-y-3 text-xs">
              
              <!-- Option 1: Ví Điện Tử MoMo / MoMo QR -->
              <div onclick="selectPaymentMethod('bacs')" id="payOptionBACS" class="border-2 border-[#A50064] bg-[#A50064]/5 rounded-xl p-3.5 sm:p-4 cursor-pointer transition">
                <div class="flex items-center justify-between">
                  <label class="flex items-center gap-2.5 font-bold text-gray-900 cursor-pointer">
                    <input type="radio" name="checkoutPayment" id="radioPayBACS" value="bacs" checked class="accent-[#A50064] w-4 h-4 cursor-pointer">
                    <span class="flex items-center gap-2">
                      <span class="w-5 h-5 rounded-md bg-[#A50064] text-white flex items-center justify-center font-bold text-[10px]">M</span>
                      <span class="text-gray-900 font-bold">Ví Điện Tử MoMo / MoMo QR (24/7)</span>
                    </span>
                  </label>
                  <span class="text-[10px] bg-pink-100 text-[#A50064] font-extrabold px-2 py-0.5 rounded-full">Khuyên dùng</span>
                </div>
                
                <div id="bacsDetailsBox" class="mt-3 pl-6 pr-2 pt-2.5 border-t border-pink-200/60 text-[11px] text-gray-600 space-y-2">
                  <p class="leading-relaxed">
                    Hệ thống tự động tạo <strong>mã MoMo QR</strong> có sẵn số tiền và cú pháp đơn hàng của bạn. Bạn chỉ cần mở App MoMo (hoặc bất kỳ App Ngân hàng nào qua Napas) để quét trong 3 giây.
                  </p>
                  <div class="bg-white p-2.5 rounded-lg border border-pink-200 flex items-center justify-between">
                    <div>
                      <div class="text-[10px] text-gray-400">Số Ví MoMo nhận tiền:</div>
                      <div class="font-bold text-gray-900 text-xs flex items-center gap-1.5">
                        <span class="text-[#A50064] font-black">Ví MoMo:</span> <strong>0933.543.987</strong>
                      </div>
                      <div class="text-[10px] text-[#A50064] font-semibold">DUWCSANHLIB — HIỆU SÁCH TRI THỨC</div>
                    </div>
                    <span class="material-symbols-outlined text-2xl text-emerald-600">verified</span>
                  </div>
                </div>
              </div>

              <!-- Option 2: COD (Thanh toán khi nhận sách) -->
              <div onclick="selectPaymentMethod('cod')" id="payOptionCOD" class="border border-gray-200 bg-white hover:border-gray-300 rounded-xl p-3.5 sm:p-4 cursor-pointer transition">
                <div class="flex items-center justify-between">
                  <label class="flex items-center gap-2.5 font-bold text-gray-900 cursor-pointer">
                    <input type="radio" name="checkoutPayment" id="radioPayCOD" value="cod" class="accent-brand-red w-4 h-4 cursor-pointer">
                    <span class="flex items-center gap-1.5">
                      <span class="material-symbols-outlined text-amber-600 text-base">local_shipping</span>
                      <span>Thanh toán khi nhận sách (COD)</span>
                    </span>
                  </label>
                  <span class="text-[10px] bg-gray-100 text-gray-600 font-semibold px-2 py-0.5 rounded-full">Tiền mặt</span>
                </div>

                <div id="codDetailsBox" class="hidden mt-3 pl-6 pr-2 pt-2.5 border-t border-gray-100 text-[11px] text-gray-600 space-y-1.5">
                  <p class="leading-relaxed">
                    Bạn chỉ phải thanh toán tiền mặt trực tiếp cho nhân viên bưu tá khi ấn phẩm được giao đến tận nhà. Quý khách được phép kiểm tra sách còn nguyên màng co bảo vệ trước khi nhận.
                  </p>
                </div>
              </div>

            </div>
          </div>

        </div>

        <!-- Right Column: Order Summary (Flatsome Sticky Box, 5 Cols) -->
        <div class="lg:col-span-5 space-y-4">
          <div class="bg-white rounded-2xl p-4 sm:p-6 border border-gray-200 shadow-sm sticky top-24 space-y-4">
            
            <div class="flex items-center justify-between pb-3 border-b border-gray-100">
              <h3 class="text-sm sm:text-base font-black text-gray-900 uppercase flex items-center gap-2">
                <span>ĐƠN HÀNG CỦA BẠN</span>
                <span id="checkoutItemCountBadge" class="text-xs font-bold px-2 py-0.5 rounded-full bg-red-100 text-brand-red">0 cuốn</span>
              </h3>
              <button onclick="openCart()" class="text-xs text-brand-red hover:underline font-bold flex items-center gap-0.5 cursor-pointer">
                <span class="material-symbols-outlined text-sm">edit</span>
                <span>Sửa giỏ hàng</span>
              </button>
            </div>

            <!-- Items List -->
            <div id="checkoutCartItems" class="divide-y divide-gray-100 max-h-60 overflow-y-auto pr-1 space-y-1">
              <!-- Populated by JS -->
            </div>

            <!-- Voucher Code Box -->
            <div class="pt-2 border-t border-gray-100 space-y-2">
              <label class="block text-xs font-bold text-gray-700">Mã giảm giá / Ưu đãi</label>
              <div class="flex gap-2">
                <input type="text" id="checkoutVoucherInput" placeholder="Nhập mã (DUWCSANH10 hoặc TRIAN)" class="flex-1 px-3 py-2 bg-gray-50 border border-gray-200 rounded-xl text-xs uppercase font-mono outline-none focus:border-brand-red">
                <button onclick="applyCheckoutVoucher()" class="px-4 py-2 bg-stone-800 hover:bg-black text-white text-xs font-bold rounded-xl transition cursor-pointer shrink-0">Áp dụng</button>
              </div>
              <div class="flex items-center gap-1.5 flex-wrap text-[11px] text-gray-500">
                <span>Gợi ý:</span>
                <button onclick="setCheckoutVoucher('DUWCSANH10')" class="px-2 py-0.5 bg-red-50 text-brand-red font-mono font-bold rounded hover:bg-red-100 transition cursor-pointer">DUWCSANH10 (-10%)</button>
                <button onclick="setCheckoutVoucher('TRIAN')" class="px-2 py-0.5 bg-amber-50 text-amber-800 font-mono font-bold rounded hover:bg-amber-100 transition cursor-pointer">TRIAN (-20K)</button>
              </div>
            </div>

            <!-- Cost Breakdown -->
            <div class="pt-3 border-t border-gray-100 space-y-2 text-xs text-gray-600">
              <div class="flex justify-between">
                <span>Tạm tính sách:</span>
                <span id="checkoutSubtotalDisplay" class="font-bold text-gray-900">0 đ</span>
              </div>
              <div class="flex justify-between">
                <span>Giảm giá voucher:</span>
                <span id="checkoutDiscountDisplay" class="font-bold text-emerald-600">0 đ</span>
              </div>
              <div class="flex justify-between">
                <span>Phí vận chuyển:</span>
                <span id="checkoutShippingDisplay" class="font-bold text-gray-900">25.000 đ</span>
              </div>

              <!-- Freeship status indicator -->
              <div id="checkoutFreeshipTag" class="text-[11px] text-emerald-700 bg-emerald-50 px-2.5 py-1.5 rounded-lg border border-emerald-200 flex items-center gap-1.5 font-medium">
                <span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span>
                <span id="checkoutFreeshipMsg">Đơn từ 250.000 đ được miễn phí vận chuyển</span>
              </div>

              <div class="flex justify-between items-baseline pt-3 border-t border-gray-200">
                <span class="text-sm font-black text-gray-900">TỔNG THANH TOÁN:</span>
                <span id="checkoutTotalDisplay" class="text-xl sm:text-2xl font-black text-brand-red">0 đ</span>
              </div>
            </div>

            <!-- Big Submit Order Button -->
            <button onclick="processFullCheckout()" class="w-full py-3.5 bg-brand-red hover:bg-red-700 text-white font-black rounded-xl text-xs sm:text-sm uppercase tracking-wider shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer">
              <span class="material-symbols-outlined text-base">verified_user</span>
              <span>XÁC NHẬN ĐẶT HÀNG NGAY</span>
            </button>

            <!-- Flatsome Security & Trust Badges -->
            <div class="pt-3 border-t border-gray-100 grid grid-cols-3 gap-2 text-center text-[10px] text-gray-500 font-medium">
              <div class="space-y-1">
                <span class="material-symbols-outlined text-brand-red text-base">verified</span>
                <div>100% Sách Thật NXB Trẻ</div>
              </div>
              <div class="space-y-1">
                <span class="material-symbols-outlined text-amber-600 text-base">package_2</span>
                <div>Bọc Chống Sốc An Toàn</div>
              </div>
              <div class="space-y-1">
                <span class="material-symbols-outlined text-emerald-600 text-base">restart_alt</span>
                <div>Đổi Trả 7 Ngày Miễn Phí</div>
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>

    <!-- VIEW: ORDER SUCCESS / THANK YOU (FLATSOME STYLE WITH DYNAMIC MOMO QR) -->
    <div id="view-order-success" class="hidden space-y-6 max-w-4xl mx-auto w-full px-2 sm:px-4">
      
      <!-- Flatsome Step Process Indicator (Step 3 Complete) -->
      <div class="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm">
        <div class="flex items-center justify-center gap-2 sm:gap-6 text-[11px] sm:text-xs font-bold uppercase tracking-wider">
          <div class="flex items-center gap-1.5 text-gray-400">
            <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-[10px] sm:text-xs font-bold">✓</span>
            <span>Giỏ hàng</span>
          </div>
          <span class="material-symbols-outlined text-gray-300 text-sm">chevron_right</span>
          <div class="flex items-center gap-1.5 text-gray-400">
            <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-[10px] sm:text-xs font-bold">✓</span>
            <span>Thông tin &amp; Thanh toán</span>
          </div>
          <span class="material-symbols-outlined text-gray-300 text-sm">chevron_right</span>
          <div class="flex items-center gap-1.5 text-emerald-600 font-black">
            <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] sm:text-xs font-bold shadow-sm">3</span>
            <span>Hoàn tất đơn hàng</span>
          </div>
        </div>
      </div>

      <!-- Main Thank-You Card -->
      <div class="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-6 text-center">
        
        <div class="w-16 h-16 sm:w-20 sm:h-20 mx-auto rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center ring-8 ring-emerald-50/50">
          <span class="material-symbols-outlined text-4xl sm:text-5xl">check_circle</span>
        </div>

        <div class="space-y-1.5">
          <span class="text-xs font-extrabold uppercase text-emerald-600 tracking-wider">Giao dịch thành công</span>
          <h2 class="text-xl sm:text-2xl font-black text-gray-900 uppercase">CẢM ƠN BẠN. ĐƠN HÀNG ĐÃ ĐƯỢC TIẾP NHẬN!</h2>
          <p class="text-xs sm:text-sm text-gray-600 max-w-lg mx-auto">DuwcsAnhLib đã gửi email xác nhận và đang tiến hành chuẩn bị các ấn phẩm sách tuyển chọn cho bạn.</p>
        </div>

        <!-- Flatsome 4-Column Meta Card -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-stone-50 rounded-xl p-4 border border-stone-200 text-left text-xs">
          <div>
            <div class="text-[10px] text-gray-400 uppercase font-semibold">Mã đơn hàng:</div>
            <div id="succOrderCode" class="font-mono font-black text-brand-red text-sm sm:text-base">#DAL-8899</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-400 uppercase font-semibold">Ngày đặt:</div>
            <div id="succOrderDate" class="font-bold text-gray-800">05/11/2026</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-400 uppercase font-semibold">Tổng cộng:</div>
            <div id="succOrderTotal" class="font-black text-brand-red text-sm sm:text-base">215.000 đ</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-400 uppercase font-semibold">Phương thức:</div>
            <div id="succOrderMethod" class="font-bold text-gray-800">Ví MoMo / MoMo QR</div>
          </div>
        </div>

        <!-- Dynamic MoMo QR Section (Displayed when MoMo is selected) -->
        <div id="succVietQRSection" class="p-5 sm:p-6 bg-gradient-to-br from-pink-50/70 to-red-50/60 rounded-2xl border-2 border-pink-300 text-left space-y-4">
          <div class="flex items-center gap-3 pb-3 border-b border-pink-200">
            <span class="w-8 h-8 rounded-lg bg-[#A50064] text-white flex items-center justify-center font-bold text-sm shadow">M</span>
            <div>
              <h4 class="font-black text-gray-900 text-sm sm:text-base uppercase flex items-center gap-2">
                <span>Thanh toán qua Ví Điện Tử MoMo</span>
                <span class="text-[10px] bg-pink-100 text-[#A50064] font-extrabold px-2 py-0.5 rounded-full">Quét mã 24/7</span>
              </h4>
              <p class="text-[11px] text-gray-500">Mở App MoMo (hoặc bất kỳ App Ngân hàng nào qua Napas) để quét mã thanh toán tức thì</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-12 gap-5 items-center">
            
            <!-- Dynamic QR Code Image -->
            <div class="md:col-span-5 flex flex-col items-center justify-center p-3 bg-white rounded-xl border border-pink-200 shadow-sm">
              <img id="succVietQRImage" src="" alt="Mã QR MoMo DuwcsAnhLib" class="w-48 h-48 sm:w-56 sm:h-56 object-contain rounded-lg">
              <div class="mt-2 text-[10px] text-[#A50064] font-bold">Mở App MoMo hoặc Ngân hàng để quét</div>
              <a id="btnOpenMoMoApp" href="https://me.momo.vn/0933543987" target="_blank" class="mt-2 w-full py-1.5 bg-[#A50064] hover:bg-[#860050] text-white text-[11px] font-bold rounded-lg text-center transition shadow-sm flex items-center justify-center gap-1">
                <span>Mở nhanh App MoMo</span>
                <span class="material-symbols-outlined text-xs">open_in_new</span>
              </a>
            </div>

            <!-- Transfer Info Cards with 1-Click Copy Buttons -->
            <div class="md:col-span-7 space-y-2.5 text-xs">
              <div class="p-2.5 bg-white rounded-xl border border-gray-200 flex items-center justify-between">
                <div>
                  <div class="text-[10px] text-gray-400">Hình thức nhận:</div>
                  <div class="font-bold text-gray-900 flex items-center gap-1.5">
                    <span class="w-3.5 h-3.5 rounded bg-[#A50064] text-white text-[9px] flex items-center justify-center font-bold">M</span>
                    <span>Ví Điện Tử MoMo (CTCP Dịch Vụ Di Động Trực Tuyến)</span>
                  </div>
                </div>
                <span class="text-[10px] bg-pink-100 text-[#A50064] font-bold px-2 py-0.5 rounded">MoMo 24/7</span>
              </div>

              <div class="p-2.5 bg-white rounded-xl border border-pink-300 flex items-center justify-between">
                <div>
                  <div class="text-[10px] text-gray-400">Số Ví MoMo / STK nhận:</div>
                  <div id="copyAccountNum" class="font-mono font-black text-[#A50064] text-base">0933543987</div>
                </div>
                <button onclick="copyText('0933543987', this)" class="px-3 py-1.5 bg-pink-50 hover:bg-[#A50064] hover:text-white text-[#A50064] font-bold text-xs rounded-lg transition flex items-center gap-1 cursor-pointer">
                  <span class="material-symbols-outlined text-xs">content_copy</span>
                  <span>Sao chép Ví MoMo</span>
                </button>
              </div>

              <div class="p-2.5 bg-white rounded-xl border border-gray-200 flex items-center justify-between">
                <div>
                  <div class="text-[10px] text-gray-400">Tên chủ Ví MoMo:</div>
                  <div class="font-bold text-gray-900">DUWCSANHLIB — HIỆU SÁCH TRI THỨC</div>
                </div>
              </div>

              <div class="p-2.5 bg-white rounded-xl border border-gray-200 flex items-center justify-between">
                <div>
                  <div class="text-[10px] text-gray-400">Số tiền cần chuyển:</div>
                  <div id="succCopyAmount" class="font-mono font-black text-brand-red text-sm">215.000 đ</div>
                </div>
                <button id="btnCopyAmount" onclick="copyAmount(this)" class="px-2.5 py-1 bg-red-50 hover:bg-brand-red hover:text-white text-brand-red font-bold text-[11px] rounded-lg transition flex items-center gap-1 cursor-pointer">
                  <span class="material-symbols-outlined text-xs">content_copy</span>
                  <span>Sao chép</span>
                </button>
              </div>

              <div class="p-2.5 bg-white rounded-xl border-2 border-[#A50064]/40 flex items-center justify-between">
                <div>
                  <div class="text-[10px] text-gray-400">Lời nhắn / Cú pháp chuyển MoMo:</div>
                  <div id="succCopyContent" class="font-mono font-black text-[#A50064] text-sm">DAL-8899</div>
                </div>
                <button id="btnCopyContent" onclick="copyContent(this)" class="px-2.5 py-1 bg-[#A50064] hover:bg-[#860050] text-white font-bold text-[11px] rounded-lg transition flex items-center gap-1 cursor-pointer shadow-sm">
                  <span class="material-symbols-outlined text-xs">content_copy</span>
                  <span>Sao chép lời nhắn</span>
                </button>
              </div>

              <div class="text-[11px] text-gray-500 italic pt-1">
                * Vui lòng điền đúng <strong>Lời nhắn MoMo</strong> để hệ thống tự động xác nhận đơn hàng sau 1-3 phút.
              </div>
            </div>

          </div>
        </div>

        <!-- COD Notification Section (Displayed when COD is selected) -->
        <div id="succCODSection" class="hidden p-5 sm:p-6 bg-amber-50 rounded-2xl border border-amber-200 text-left space-y-2">
          <div class="flex items-center gap-2 text-amber-800 font-bold text-sm">
            <span class="material-symbols-outlined text-amber-700">inventory_2</span>
            <span>Đơn hàng thanh toán khi nhận hàng (COD) đang được đóng gói</span>
          </div>
          <p class="text-xs text-amber-900 leading-relaxed">
            Nhân viên của DuwcsAnhLib sẽ liên hệ với bạn qua số điện thoại <strong id="succCODPhone">0933543987</strong> để xác nhận thời gian giao hàng. Bạn chỉ cần chuẩn bị số tiền mặt <strong id="succCODAmount" class="text-brand-red">0 đ</strong> để thanh toán cho bưu tá khi nhận sách.
          </p>
        </div>

        <!-- Customer Details & Items Summary -->
        <div class="text-left space-y-4 pt-2">
          <h4 class="font-black text-gray-900 text-sm uppercase pb-2 border-b border-gray-100">Chi tiết người nhận &amp; Sách đã đặt</h4>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs bg-gray-50 p-4 rounded-xl border border-gray-200">
            <div>
              <span class="text-gray-400">Người nhận:</span>
              <strong id="succCustName" class="text-gray-800 block">Nguyễn Văn An</strong>
            </div>
            <div>
              <span class="text-gray-400">Số điện thoại:</span>
              <strong id="succCustPhone" class="text-gray-800 block">0933543987</strong>
            </div>
            <div class="sm:col-span-2">
              <span class="text-gray-400">Địa chỉ giao sách:</span>
              <strong id="succCustAddress" class="text-gray-800 block">123 Nguyễn Thị Minh Khai, Q.1</strong>
            </div>
            <div class="sm:col-span-2" id="succCustNoteRow">
              <span class="text-gray-400">Ghi chú:</span>
              <span id="succCustNote" class="text-gray-700 italic block">Không có ghi chú</span>
            </div>
          </div>

          <!-- Items Table -->
          <div class="border border-gray-200 rounded-xl overflow-hidden">
            <table class="w-full text-xs text-left">
              <thead class="bg-gray-100 text-gray-600 font-bold uppercase text-[10px]">
                <tr>
                  <th class="py-2.5 px-3">Tựa sách</th>
                  <th class="py-2.5 px-3 text-center">SL</th>
                  <th class="py-2.5 px-3 text-right">Đơn giá</th>
                  <th class="py-2.5 px-3 text-right">Thành tiền</th>
                </tr>
              </thead>
              <tbody id="succItemsTableBody" class="divide-y divide-gray-100">
                <!-- Populated by JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
          <button onclick="window.print()" class="w-full sm:w-auto px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold rounded-xl transition flex items-center justify-center gap-1.5 cursor-pointer">
            <span class="material-symbols-outlined text-sm">print</span>
            <span>In đơn hàng / Hóa đơn</span>
          </button>
          <button onclick="showView('shop')" class="w-full sm:w-auto px-6 py-2.5 bg-brand-red hover:bg-red-700 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-1.5 shadow-md cursor-pointer">
            <span class="material-symbols-outlined text-sm">storefront</span>
            <span>Tiếp tục mua sắm</span>
          </button>
        </div>

      </div>

    </div>
"""

