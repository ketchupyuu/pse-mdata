colorscheme desert	    "other options: solarized,molokai
syntax enable		    "enable syntax processing

"spaces and tabs
set tabstop=4		    "visual spaces per TAB
set softtabstop=4	    "number of spaces in tab when editing
set expandtab		    "tabs are spaces

"ui config
set showcmd     "shows command at bottom right
set wildmenu    "visual autocomplete for command menu
set lazyredraw  "redraw only when we need to making it faster
set showmatch   "highlight matching [{()}]

"searching
set incsearch   "search as characters are entered
set hlsearch    "highlight matches
"turn-off search highlight
nnoremap <leader><space> :nohlsearch<CR>    

"folding
"set foldenable  "enable folding
"set foldlevelstart=1    "open most folds by default
"set foldnestmax=10      "10 nested fold max
"nnoremap <space> za
"set foldmethod=indent

"movement
"move vertically by visual line
nnoremap j gj
nnoremap k gk
"move to beginning/end of line
nnoremap B ^
nnoremap E $
"^/$ does nothing
nnoremap $ <nop>
nnoremap ^ <nop>

"highlight last inserted text
nnoremap gV `[v`]

let mapleader=","
"jk is escape
inoremap jk <esc>

"exit and save with leader
nnoremap <leader>q :q! <CR>
nnoremap <leader>a :wqa <CR>
