// V22 Connect Cheeko (Getting Started, part 3 of 4). App screens: real Flutter widgets with sample data (app-shots/setup, commit d49af42).
// Device screens: real firmware renders of the first-boot setup flow (fw-screens/setup_*, FW 2.4.311).
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en;
  const A = 'app-shots/setup/';
  const PX = 40, PY = 235, PW = 480, PH = PW * 852 / 393;
  const tapP = (fy) => [PX + PW * .5, PY + 12 + (PH - 24) * fy];          // a tap on the phone screen, fy = 0..1 from the top
  const dig = '482915', dt = (E(7) - L(7)) / 6;
  return {
    mood: 'calm', capsY: 1330, bubbleY: 1300, noBubble: [7], duoDefaults: {pw: PW, px: PX, py: PY, dw: 360, dx: 640, dy: 640}, badge: tx('GETTING STARTED · <b>3/4</b>', 'शुरुआत · <b>3/4</b>'),
    shots: [
      {t: 0, type: 'duo', bg: 'var(--sun)', app: [[0, A + 's01_walkthrough_signin.png']], dev: [[0, 'setup_2_wifi_prompt_connect']]},
      {t: L(1) - .1, type: 'duo', bg: 'var(--tint)', rays: false, step: tx('STEP <span>3</span>', 'स्टेप <span>3</span>'),
       app: [[L(1) - .1, A + 's01_walkthrough_signin.png'], [L(1) + 2.3, A + 's02_parent_consent.png']], dev: [[L(1) - .1, 'setup_2_wifi_prompt_connect']],
       taps: [[L(1) + 1.9, ...tapP(.78)]]},
      {t: L(2) - .1, type: 'duo', bg: 'var(--tint)', rays: false,
       app: [[L(2) - .1, A + 's03b_name.png'], [L(2) + .9, A + 's03c2_age_confirm.png'], [L(2) + 1.8, A + 's03e_interests.png'], [L(2) + 2.7, A + 's03g_all_set.png']],
       dev: [[L(2) - .1, 'setup_2_wifi_prompt_connect']]},
      {t: L(3) - .1, type: 'device', bg: 'var(--sun)', w: 520, y: 330, step: tx('STEP <span>4</span>', 'स्टेप <span>4</span>'), press: [L(3) + 1.3],
       screens: [[L(3) - .1, 'setup_2_wifi_prompt_connect'], [L(3) + 1.35, 'setup_3_getting_ready'], [L(3) + 2.4, 'setup_4_ble_waiting']]},
      {t: L(4) - .1, type: 'duo', bg: 'var(--tint)', rays: false,
       app: [[L(4) - .1, A + 's04_setup_checklist.png'], [L(4) + 1.0, A + 's06_scanning.png'], [L(4) + 1.9, A + 's06b_found.png']],
       dev: [[L(4) - .1, 'setup_4_ble_waiting'], [L(4) + 2.4, 'setup_4b_phone_connected']], taps: [[L(4) + 2.3, ...tapP(.53)]]},
      {t: L(5) - .1, type: 'duo', bg: 'var(--tint)', rays: false,
       app: [[L(5) - .1, A + 's07_wifi_list.png'], [L(5) + .5, A + 's07b_wifi_password.png'], [L(5) + 1.0, A + 's08_sending_bluetooth.png']],
       dev: [[L(5) - .1, 'setup_4c_credentials_received'], [L(5) + .6, 'setup_5_wifi_connecting'], [L(5) + 1.2, 'setup_5b_wifi_connected']], taps: [[L(5) + .4, ...tapP(.36)]]},
      {t: L(6) - .1, type: 'device', bg: 'var(--purple)', w: 520, y: 330, step: tx('STEP <span>5</span>', 'स्टेप <span>5</span>'), chipY: 1215,
       screens: [[L(6) - .1, 'setup_5c_all_set'], [L(6) + 1.2, 'setup_7_activation_code']],
       chips: [[L(6) + 1.2, tx('Listen 👂', 'सुनो 👂')]].concat([...dig].map((d, i) => [L(7) + i * dt, '🔢 ' + dig.slice(0, i + 1)]))},
      {t: L(8) - .1, type: 'duo', bg: 'var(--tint)', rays: false,
       app: [[L(8) - .1, A + 's09_code_empty.png'], [L(8) + .6, A + 's09_code_entered.png']], dev: [[L(8) - .1, 'setup_7_activation_code']], taps: [[L(8) + 1.4, ...tapP(.47)]]},
      {t: L(9) - .1, type: 'device', bg: 'var(--sun)', w: 520, y: 330, confetti: L(9) + .2, screens: [[L(9) - .1, 'setup_8b_ready_home_after_banner']]},
      {t: L(10) - .1, type: 'title', bg: 'var(--green)', y: 600, size: 130, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">First 5 minutes</span> <span class="e">👉</span><br><span style="font-size:60px">Part 4 of 4</span>', 'अगला:<br><span class="hl">पहले 5 मिनट</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 4 / 4</span>')},
    ],
  };
};
