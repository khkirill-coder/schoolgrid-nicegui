"""
SchoolGrid — Professional NiceGUI Edition v2.4
Fixed Overlaps | Functional Templates | "My Wave" Dark Theme
"""

import random
import json
import os
from datetime import datetime
from nicegui import ui, app

# ==================== STATE ====================
STATE = {
    'prof': {'name': '', 'school': '', 'role': '', 'cls': ''},
    'days': 5,
    'maxL': 7,
    'start': '08:00',
    'dur': 45,
    'sb': 10,
    'lb': 20,
    'la': 3,
    'subjects': [],
    'grid': {},
}

DAY_NAMES = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
COLORS = [
    '#2dd4a0', '#4a8fe7', '#d97757', '#8b5cf6', '#f59e0b',
    '#ef4444', '#14b8a6', '#ec4899', '#84cc16', '#f97316',
]

TEMPLATE_SUBJECTS = [
    ('Русский язык', 4), ('Математика', 5), ('Литература', 3),
    ('История', 2), ('Физика', 2), ('Биология', 2),
    ('География', 1), ('Английский язык', 3), ('Обществознание', 1),
    ('Информатика', 2), ('Физкультура', 3), ('Химия', 2),
]

SAVE_FILE = os.path.join(os.path.dirname(__file__), 'schoolgrid_data.json')

# ==================== HELPERS ====================
def fmt_time(total_min: int) -> str:
    return f'{(total_min // 60) % 24:02d}:{total_min % 60:02d}'

def generate_schedule():
    STATE['grid'] = {}
    pool = []
    for idx, s in enumerate(STATE['subjects']):
        pool.extend([idx] * s['hours'])
    
    random.shuffle(pool)
    day_assignments = {d: [] for d in range(STATE['days'])}
    
    for subj_idx in pool:
        cands = list(range(STATE['days']))
        random.shuffle(cands)
        best_day = -1
        min_score = 9999
        for d in cands:
            if len(day_assignments[d]) >= STATE['maxL']: continue
            score = (day_assignments[d].count(subj_idx) * 50) + len(day_assignments[d])
            if score < min_score:
                min_score = score
                best_day = d
        if best_day != -1: day_assignments[best_day].append(subj_idx)

    for d in range(STATE['days']):
        lessons = day_assignments[d]
        random.shuffle(lessons)
        for l, subj_idx in enumerate(lessons):
            STATE['grid'][f'{d}_{l}'] = subj_idx

def save_data():
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(STATE, f, ensure_ascii=False, indent=2)
    except: pass

def load_data():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                STATE.update(json.load(f))
            return True
    except: pass
    return False

# ==================== CSS ====================
CUSTOM_CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:wght@500;600&display=swap');
:root {
    --bg-deep: #000000;
    --accent-primary: #2dd4a0;
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.6);
    --border-glass: rgba(255, 255, 255, 0.1);
}
body { background: #000; font-family: 'Inter', sans-serif !important; color: #fff; }
.liquid-bg { position: fixed; inset: 0; z-index: -10; background: #000; }
.blob { position: absolute; border-radius: 50%; filter: blur(140px); opacity: 0.25; mix-blend-mode: screen; }
.blob-1 { background: #2dd4a0; width: 70vw; height: 70vw; top: -10%; left: -20%; animation: move 25s infinite alternate; }
.blob-2 { background: #4a8fe7; width: 70vw; height: 70vw; bottom: -10%; right: -20%; animation: move 30s infinite alternate-reverse; }
.blob-3 { background: #8b5cf6; width: 40vw; height: 40vw; top: 30%; left: 30%; filter: blur(180px); }
@keyframes move { from { transform: translate(0,0) scale(1); } to { transform: translate(10%, 10%) scale(1.1); } }
.vignette { position: fixed; inset: 0; z-index: -9; background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.9) 100%); }

.glass-card { 
    background: rgba(15, 15, 22, 0.7) !important; 
    backdrop-filter: blur(50px) saturate(160%) brightness(1.2);
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 32px !important;
    padding: 40px !important;
}
.logo-text { font-family: 'Lora', serif; font-size: 32px; font-weight: 600; background: linear-gradient(135deg, #2dd4a0, #4a8fe7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.btn-primary { background: #fff !important; color: #000 !important; border-radius: 100px !important; font-weight: 700 !important; cursor: pointer; border: none !important; padding: 12px 32px !important; transition: 0.3s; }
.btn-primary:hover { transform: scale(1.03); box-shadow: 0 0 20px rgba(255,255,255,0.2); }
.btn-ghost { background: rgba(255,255,255,0.05) !important; color: #fff !important; border-radius: 100px !important; border: 1px solid rgba(255,255,255,0.1) !important; cursor: pointer; transition: 0.3s; }
.btn-ghost:hover { background: rgba(255,255,255,0.1) !important; border-color: rgba(255,255,255,0.3); }

/* Input Fixes */
.input-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: rgba(255,255,255,0.4); margin-bottom: 6px; margin-left: 4px; }
.glass-input .q-field__control { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; height: 52px !important; }
.glass-input .q-field__native, .glass-input input { color: #fff !important; padding: 0 16px !important; }
.glass-input .q-field__control::before, .glass-input .q-field__control::after { display: none !important; }

.schedule-cell { background: rgba(255,255,255,0.02); border: 1px solid var(--border-glass); border-radius: 16px; padding: 12px; min-height: 85px; transition: 0.3s; cursor: pointer; }
.schedule-cell.filled { border-left: 4px solid var(--cell-accent, #2dd4a0); background: rgba(255,255,255,0.04); }
.noise-overlay { position: fixed; inset: 0; z-index: -8; background: url('https://grainy-gradients.vercel.app/noise.svg'); opacity: 0.05; pointer-events: none; mix-blend-mode: overlay; }
'''

# ==================== UI ====================
@ui.page('/')
def main_page():
    ui.add_head_html(f'<style>{CUSTOM_CSS}</style>')
    ui.add_body_html('''
        <div class="noise-overlay"></div>
        <div class="liquid-bg">
            <div class="blob blob-1"></div>
            <div class="blob blob-2"></div>
            <div class="blob blob-3"></div>
            <div class="vignette"></div>
        </div>
    ''')

    views = {}
    def show_view(name):
        for k, v in views.items(): v.set_visibility(k == name)

    # 1. WELCOME
    with ui.column().classes('fixed inset-0 items-center justify-center z-10') as welcome_view:
        views['welcome'] = welcome_view
        with ui.card().classes('glass-card text-center').style('width:480px'):
            ui.html('<div class="logo-text" style="margin-bottom:8px">School<span>Grid</span></div>')
            ui.label('Простой и мощный генератор расписания.').classes('text-white opacity-50 mb-10 text-lg')
            ui.button('Начать работу', on_click=lambda: show_view('profile')).classes('btn-primary w-full h-14 text-lg')
            ui.button('Загрузить сохранение', on_click=lambda: load_and_show()).classes('btn-ghost w-full mt-4 h-12')
            ui.html('''
                <div style="margin-top:48px; font-size:11px; color:rgba(255,255,255,0.25); text-align:center;">
                    by <a href="https://aktrons.netlify.app" target="_blank" style="color:#2dd4a0; text-decoration:none; font-weight:700">Aktrons</a>
                </div>
            ''')

    # 2. PROFILE
    with ui.column().classes('fixed inset-0 items-center justify-center z-10') as profile_view:
        views['profile'] = profile_view
        profile_view.set_visibility(False)
        with ui.card().classes('glass-card').style('width:640px'):
            ui.label('Твой Профиль').classes('text-3xl text-white font-serif mb-10')
            
            with ui.column().classes('w-full gap-5 mb-10'):
                with ui.column().classes('w-full gap-1'):
                    ui.label('Твое Имя').classes('input-label')
                    p_name = ui.input(placeholder='Иван Иванов').classes('glass-input w-full')
                with ui.column().classes('w-full gap-1'):
                    ui.label('Учебное заведение').classes('input-label')
                    p_school = ui.input(placeholder='Гимназия №1').classes('glass-input w-full')
                with ui.row().classes('w-full gap-5'):
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Должность').classes('input-label')
                        p_role = ui.input(placeholder='Учитель').classes('glass-input w-full')
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Класс').classes('input-label')
                        p_cls = ui.input(placeholder='10-А').classes('glass-input w-full')
            
            with ui.row().classes('w-full justify-between pt-8 border-t border-white/10'):
                ui.button('Назад', on_click=lambda: show_view('welcome')).classes('btn-ghost px-8')
                def save_prof():
                    STATE['prof'].update({'name': p_name.value, 'school': p_school.value, 'role': p_role.value, 'cls': p_cls.value})
                    show_view('wizard')
                ui.button('Продолжить', on_click=save_prof).classes('btn-primary px-10')

    # 3. WIZARD
    wizard_step = {'v': 1}
    with ui.column().classes('fixed inset-0 items-center justify-center z-10 p-6 overflow-auto') as wizard_view:
        views['wizard'] = wizard_view
        wizard_view.set_visibility(False)
        with ui.card().classes('glass-card').style('width:780px'):
            
            # --- STEP 1: BELLS ---
            with ui.column().classes('w-full') as step1:
                ui.label('Структура занятий').classes('text-2xl text-white font-serif mb-8 text-center w-full')
                with ui.row().classes('w-full gap-5 mb-5'):
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Рабочих дней').classes('input-label')
                        i_days = ui.select({5: '5 дней (Пн-Пт)', 6: '6 дней (Пн-Сб)'}, value=5).classes('glass-input w-full')
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Уроков в день').classes('input-label')
                        i_max = ui.number(value=7, min=1, max=12).classes('glass-input w-full')
                with ui.row().classes('w-full gap-5 mb-10'):
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Первый урок').classes('input-label')
                        i_start = ui.input(value='08:00').classes('glass-input w-full')
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Длительность (мин)').classes('input-label')
                        i_dur = ui.number(value=45).classes('glass-input w-full')
            
            # --- STEP 2: SUBJECTS ---
            with ui.column().classes('w-full') as step2:
                step2.set_visibility(False)
                ui.label('Дисциплины').classes('text-2xl text-white font-serif mb-8 text-center w-full')
                
                ui.button('Использовать школьный шаблон', on_click=lambda: apply_template()).classes('btn-ghost w-full mb-6 h-12')
                
                subj_list_cont = ui.column().classes('w-full gap-3 max-h-64 overflow-auto pr-3 mb-6')
                
                def refresh_subj_ui():
                    subj_list_cont.clear()
                    with subj_list_cont:
                        for idx, s in enumerate(STATE['subjects']):
                            with ui.row().classes('w-full items-center p-3 rounded-2xl bg-white/5 border border-white/5'):
                                ui.html(f'<div style="width:10px;height:10px;border-radius:50%;background:{s["color"]}"></div>')
                                ui.label(s['name']).classes('flex-1 text-white font-bold ml-2')
                                ui.label(f"{s['hours']} ч.").classes('text-white opacity-40 mr-4')
                                def delete_s(i=idx):
                                    STATE['subjects'].pop(i)
                                    refresh_subj_ui()
                                ui.button('×', on_click=delete_s).classes('text-red-400 bg-transparent text-xl font-bold')

                def apply_template():
                    STATE['subjects'] = []
                    for n, h in TEMPLATE_SUBJECTS:
                        STATE['subjects'].append({'name': n, 'hours': h, 'color': COLORS[len(STATE['subjects']) % len(COLORS)]})
                    refresh_subj_ui()
                    ui.notify('Шаблон применен успешно')

            # --- STEP 3: SUMMARY ---
            with ui.column().classes('w-full items-center') as step3:
                step3.set_visibility(False)
                ui.label('Все готово!').classes('text-3xl text-white font-serif mb-10')
                
                with ui.row().classes('w-full gap-4 mb-12'):
                    for l, v in [('Дней', f"{i_days.value}"), ('Макс. уроков', f"{i_max.value}"), ('Предметов', f"{len(STATE['subjects'])}")]:
                        with ui.column().classes('flex-1 p-5 rounded-3xl bg-white/3 border border-white/5 text-center'):
                            ui.label(l).classes('text-[10px] uppercase tracking-widest opacity-30 mb-2')
                            ui.label(v).classes('text-3xl font-bold text-white')
                
                ui.button('Сгенерировать расписание', on_click=lambda: launch_app()).classes('btn-primary px-16 h-16 text-xl')

            steps = [step1, step2, step3]
            
            # Nav Footer
            with ui.row().classes('w-full justify-between mt-10 pt-8 border-t border-white/10'):
                btn_prev = ui.button('Назад', on_click=lambda: nav(-1)).classes('btn-ghost px-8')
                btn_prev.set_visibility(False)
                btn_next = ui.button('Продолжить', on_click=lambda: nav(1)).classes('btn-primary px-10')

            def nav(d):
                v = wizard_step['v'] + d
                if v < 1 or v > 3: return
                wizard_step['v'] = v
                for i, s in enumerate(steps): s.set_visibility(i+1 == v)
                btn_prev.set_visibility(v > 1)
                btn_next.set_visibility(v < 3)
                if v == 2: refresh_subj_ui()

    # 4. DASHBOARD
    table_render_cont = None
    with ui.column().classes('fixed inset-0 z-10 overflow-auto') as main_view:
        views['main'] = main_view
        main_view.set_visibility(False)
        
        with ui.row().classes('w-full p-6 justify-between items-center border-b border-white/10 max-w-[1240px] mx-auto'):
            ui.html('<div class="logo-text" style="font-size:24px">School<span>Grid</span></div>')
            with ui.row().classes('gap-3'):
                ui.button('Настройки', on_click=lambda: show_view('wizard')).classes('btn-ghost px-5 h-11')
                ui.button('Сохранить .txt', on_click=lambda: ui.download(build_export_txt().encode('utf-8-sig'), 'schedule.txt')).classes('btn-ghost px-5 h-11')
                ui.button('Перегенерировать', on_click=lambda: (generate_schedule(), render_schedule())).classes('btn-primary px-8 h-11')

        with ui.column().classes('w-full p-10 max-w-[1240px] mx-auto'):
            prof_title = ui.label('').classes('text-4xl text-white font-serif mb-2')
            prof_stats = ui.label('').classes('text-white opacity-40 mb-12 text-base')
            table_render_cont = ui.column().classes('w-full overflow-x-auto pb-24')

    def render_schedule():
        table_render_cont.clear()
        prof_title.set_text(f"{STATE['prof']['cls']} • Расписание")
        prof_stats.set_text(f"{STATE['prof']['name']} • {STATE['prof']['school']} • {STATE['days']} дней")
        
        with table_render_cont:
            # Header
            with ui.row().classes('w-full gap-4 mb-5'):
                ui.label('').style('width:80px')
                for d in range(STATE['days']):
                    ui.label(DAY_NAMES[d]).classes('flex-1 text-white font-serif text-xl opacity-60 text-center')
            
            # Grid
            h, m = map(int, STATE['start'].split(':'))
            total_t = h * 60 + m
            for l in range(STATE['maxL']):
                s_t, e_t = fmt_time(total_t), fmt_time(total_t + STATE['dur'])
                with ui.row().classes('w-full gap-4 mb-4 items-stretch'):
                    # Time Column
                    with ui.column().style('width:80px; text-align:center; justify-content:center'):
                        ui.label(s_t).classes('text-white font-bold text-sm')
                        ui.label(e_t).classes('text-white text-[11px] opacity-30')
                    
                    for d in range(STATE['days']):
                        key = f'{d}_{l}'
                        idx = STATE['grid'].get(key)
                        subj = STATE['subjects'][idx] if idx is not None and idx < len(STATE['subjects']) else None
                        
                        cell = ui.column().classes('schedule-cell flex-1')
                        if subj:
                            cell.classes('filled').style(f'--cell-accent: {subj["color"]}')
                            with cell.on('click', lambda dd=d, ll=l: open_cell_picker(dd, ll)):
                                ui.label(subj['name']).classes('text-white font-bold text-[14px] leading-tight')
                                ui.label(f'{s_t} — {e_t}').classes('text-white opacity-30 text-[10px] mt-auto')
                        else:
                            with cell.on('click', lambda dd=d, ll=l: open_cell_picker(dd, ll)):
                                ui.label('—').classes('text-white opacity-5 m-auto text-2xl')
                
                total_t += STATE['dur'] + (STATE['lb'] if (l + 1) == STATE['la'] else STATE['sb'])

    def open_cell_picker(d, l):
        with ui.dialog() as dlog, ui.card().classes('glass-card p-10').style('width:420px'):
            ui.label('Выбор предмета').classes('text-2xl text-white font-serif mb-8 text-center w-full')
            with ui.column().classes('w-full gap-3 max-h-96 overflow-auto'):
                ui.button('Удалить из ячейки', on_click=lambda: (STATE['grid'].pop(f'{d}_{l}', None), dlog.close(), render_schedule())).classes('btn-ghost w-full text-red-400 h-12')
                for i, s in enumerate(STATE['subjects']):
                    with ui.button(on_click=lambda idx=i: (STATE['grid'].update({f'{d}_{l}': idx}), dlog.close(), render_schedule())).classes('btn-ghost w-full items-center justify-start h-14'):
                        ui.html(f'<div style="width:12px;height:12px;border-radius:50%;background:{s["color"]};margin-right:16px"></div>')
                        ui.label(s['name']).classes('flex-1 text-left font-bold text-sm')
            ui.button('Закрыть', on_click=dlog.close).classes('btn-ghost w-full mt-6 h-12')
        dlog.open()

    def build_export_txt():
        sep = '═' * 60
        thin = '─' * 60
        lines = [sep, f"{'РАСПИСАНИЕ ЗАНЯТИЙ':^60}", sep, ""]
        lines.append(f"  Класс: {STATE['prof']['cls'] or '—'}  |  Школа: {STATE['prof']['school'] or '—'}")
        lines.append(f"  Учитель: {STATE['prof']['name'] or '—'}")
        lines.append("")
        
        h, m = map(int, STATE['start'].split(':'))
        t = h * 60 + m
        for d in range(STATE['days']):
            lines.append(f"\n  ▎ {DAY_NAMES[d].upper()}")
            lines.append(f"  {thin}")
            dt = h * 60 + m
            for l in range(STATE['maxL']):
                idx = STATE['grid'].get(f'{d}_{l}')
                subj = STATE['subjects'][idx]['name'] if idx is not None else "—"
                lines.append(f"    {l+1}. {fmt_time(dt)}–{fmt_time(dt+STATE['dur'])}  │  {subj}")
                dt += STATE['dur'] + (STATE['lb'] if (l + 1) == STATE['la'] else STATE['sb'])
        lines.extend(["", thin, f"{'aktrons.netlify.app':^60}", sep])
        return "\n".join(lines)

    def launch_app():
        STATE['days'], STATE['maxL'] = i_days.value, i_max.value
        STATE['start'], STATE['dur'] = i_start.value, i_dur.value
        generate_schedule()
        render_schedule()
        save_data()
        show_view('main')

    def load_and_show():
        if load_data():
            render_schedule()
            show_view('main')

# ==================== RUN ====================
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='SchoolGrid v2.4', dark=True, native=True, window_size=(1280, 856))
