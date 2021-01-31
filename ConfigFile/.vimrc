"==================================
"Vundle.vim
"==================================

set nocompatible
filetype off


set rtp+=~/.vim/bundle/Vundle.vim
"call vundle#begin()

"Plugin 'VundleVim/Vundle.vim'
"
"Plugin 'Valloric/YouCompleteMe'
"Plugin 'scrooloose/nerdtree'                " file/directory treee
"Plugin 'scrooloose/nerdcommenter'           " code commenter
"Plugin 'kien/ctrlp.vim'                     " Fuzzy file, buffer, mru, tag, etc finder
"Plugin 'altercation/vim-colors-solarized'   " solarized theme
"Plugin 'vim-scripts/indentpython.vim'
"Plugin 'scrooloose/syntastic'
"Plugin 'nvie/vim-flake8'
"Plugin 'jnurmine/Zenburn'
"Plugin 'davidhalter/jedi-vim'
"Plugin 'tenfyzhong/CompleteParameter.vim'
"
"call vundle#end()
"
"let g:ycm_global_ycm_extra_conf = '/home/z/.vim/bundle/YouCompleteMe/.ycm_extra_conf.py'


filetype plugin indent on      "detect filetype automatically






"=================================
"=================================


syntax enable   
syntax on
set number
set smartindent                "automatic index in the new line
set hlsearch                   "high light the search
set mouse=a                    "use mouse to locate 
set showtabline=1              "show tabline when the number of tabs > 1
set completeopt-=preview       "close the Scratch window
set ic




"==============================
"Shortcut key for tabs
"==============================

:nn <M-1> 1gt 
:nn <M-2> 2gt 
:nn <M-3> 3gt 
:nn <M-4> 4gt 
:nn <M-5> 5gt 
:nn <M-6> 6gt 
:nn <M-7> 7gt 
:nn <M-8> 8gt 
:nn <M-9> 9gt 
:nn <M-0> :tablast<CR> 

noremap <C-L> <Esc>:tabnext<CR>
noremap <C-H> <Esc>:tabprevious<CR>



"=============================
"python
"=============================

set tabstop=4
set shiftwidth=4
set expandtab     "tab -> space blank 
set softtabstop=4

set encoding=utf-8
let python_highlight_all=1
syntax on

"au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/






"==============================
"FORTRAN
"==============================

let fortran_have_tabs=1
"set fileencodings=urf-8,gb18030,utf-16,big5
let fortran_fold=1
set foldmethod=syntax
set foldlevelstart=99



"===============================
"Quickly Run
"================================
map <F5> :call CompileRunGcc()<CR>
func! CompileRunGcc()
    exec "w"
    if &filetype == 'c'
        exec "!g++ % -o %<"
        exec "!time ./%<"
    elseif &filetype == 'cpp'
        exec "!g++ % -o %<"
        exec "!time ./%<"
    elseif &filetype == 'java'
        exec "!javac %"
        exec "!time java %<"
    elseif &filetype == 'sh'
        :!time bash %
    elseif &filetype == 'python'
        exec "!time python3 %"
    elseif &filetype == 'html'
        exec "!firefox % &"
    elseif &filetype == 'go'
        exec "!go build %<"
        exec "!time go run %"
    elseif &filetype == 'mkd'
        exec "!~/.vim/markdown.pl % > %.html &"
        exec "!firefox %.html &"
    endif
endfunc
