" auto-install vim-plug
if empty(glob('~/.config/nvim/autoload/plug.vim'))
    silent !curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    autocmd VimEnter * PlugInstall
endif
call plug#begin('~/.config/nvim/plugged')

Plug 'scrooloose/nerdtree'
Plug 'scrooloose/nerdcommenter'
Plug 'tpope/vim-sleuth'
Plug 'tpope/vim-surround'
Plug 'ervandew/supertab'
Plug 'vim-python/python-syntax'
Plug 'vimwiki/vimwiki'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
Plug 'ryanoasis/vim-devicons'
Plug 'dylanaraps/wal'
Plug 'ap/vim-css-color'

call plug#end()

" Other stuff ->

syntax on
set nocompatible
filetype plugin indent on
set tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab
set backspace=indent,eol,start
set number
set laststatus=2
set background=dark
set number relativenumber
set t_Co=256
let g:rehash256=1

" Disable beeps
set noerrorbells visualbell t_vb=
autocmd GUIEnter * set visualbell t_vb=

set termencoding=utf-8
colorscheme wal

" Supertab
let g:SuperTabDefaultCompletionType = "<c-n>"

" Key mappings
let mapleader="\<SPACE>"

map <Leader>n :NERDTreeToggle<CR>

nmap <Leader>j <C-W>j
nmap <Leader>k <C-W>k
nmap <Leader>h <C-W>h
nmap <Leader>l <C-W>l

" Convenience
nmap <Leader>s :w<CR>
nmap <Leader>q :wq<CR>
nmap <Leader>fq :q!<CR>
nmap <Leader>r :source %<CR>

nmap <Leader>vs :vsplit<CR>
nmap <Leader>hs :split<CR>
nnoremap ; :

" Clearing issues with tmux, set this here
set t_ut=

