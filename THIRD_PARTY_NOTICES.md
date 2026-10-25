# Third-party notices

Tindahan System's own code is licensed under MIT (see LICENSE). Dependencies retain their own copyrights and licenses. These notices cover the reviewed Linux desktop distribution; an individual setup/uninstall runtime uses a subset of these components. See third-party-manifest.json for versions, origins and SHA-256 hashes.

Pygame is used for optional checkout audio and is covered by the GNU Lesser General Public License, version 2.1 or later. Copyright (C) 2000-2001 Pete Shinners, with additional contributors identified in the source. Its license and retained helper notices are reproduced below. The app includes the corresponding Pygame source and this application's source in sources/Tindahan-System-<version>-sources.tar.gz. See SOURCE_CODE.md for modification and rebuild instructions.

You may modify the application for your own use and reverse engineer it to debug such modifications. Nothing in the application's terms restricts rights granted by the LGPL.

This software is based in part on the work of the Independent JPEG Group.

Portions of this software are copyright © 1996-2026 The FreeType Project (https://freetype.org). All rights reserved. FreeType is distributed here under the FreeType License (FTL), rather than its alternative GPL terms.

Zstandard's BSD license and libuuid's BSD terms are selected. GCC runtime libraries retain the GPL with GCC Runtime Library Exception; the exception permits eligible independently compiled applications to use their own license. PyInstaller's bootloader exception is also preserved.

The unused GNU Readline extension/library and Pygame FreeSans font are excluded from this distribution.

## dav1d (inside libavif) — 1.5.3 (b546257)

License: BSD-2-Clause

Upstream: https://code.videolan.org/videolan/dav1d

### licenses/pillow-dav1d/COPYING

```text
Copyright © 2018-2025, VideoLAN and dav1d authors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-dav1d/THANKS.md

```text
# The dav1d project and VideoLAN association would like to thank

## AOM
The Alliance for Open Media (AOM) for partially funding this project.

## Companies
* Two Orioles LLC, for important coding effort
* VideoLabs SAS

## Projects
* VideoLAN
* FFmpeg
* libplacebo

## Individual

And all the dav1d Authors (git shortlog -sn), including:

Henrik Gramner, Martin Storsjö, Ronald S. Bultje, Janne Grunau, James Almer,
Victorien Le Couviour--Tuffet, Matthias Dressel, Nathan E. Egge,
Jean-Baptiste Kempf, Marvin Scholz, Luc Trudeau, Niklas Haas,
Hugo Beauzée-Luyssen, Konstantin Pavlov, David Michael Barr, Steve Lhomme,
yuanhecai, Luca Barbato, Wan-Teh Chang, Kyle Siefring, B Krishnan Iyer,
Francois Cartegnie, Liwei Wang, David Conrad, Derek Buitenhuis, Jan Beich,
Michael Bradshaw, Raphaël Zumer, Xuefeng Jiang, Arpad Panyik, Christophe Gisquet,
Justin Bull, Boyuan Xiao, Dale Curtis, Emmanuel Gil Peyrot, Raphael Zumer,
Rupert Swarbrick, Thierry Foucu, Thomas Daede, jinbo, André Kempe, Colin Lee,
Jonathan Wright, Lynne, Michail Alvanos, Nico Weber, Salome Thirot, SmilingWolf,
Tristan Laurent, Tristan Matthews, Vittorio Giovara, Yannis Guyon,
Andrey Semashev, Anisse Astier, Anton Mitrofanov, Charlie Hayden, Dmitriy Sychov,
Ewout ter Hoeven, Fred Barbier, Hao Chen, Jean-Yves Avenard, Joe Drago,
Mark Shuttleworth, Matthieu Bouron, Mehdi Sabwat, Nicolas Frattaroli,
Pablo Stebler, Rostislav Pehlivanov, Sebastian Dröge, Shiz, Steinar Midtskogen,
Sylvain BERTRAND, Sylvestre Ledru, Timo Gurr, Vibhoothi,
Vignesh Venkatasubramanian, Xavier Claessens, Xu Guangxin, kossh1 and skal.
```

### licenses/pillow-dav1d/x86inc-notice.txt

```text
;*****************************************************************************
;* x86inc.asm: x86 abstraction layer
;*****************************************************************************
;* Copyright (C) 2005-2024 x264 project
;*
;* Authors: Loren Merritt <lorenm@u.washington.edu>
;*          Henrik Gramner <henrik@gramner.com>
;*          Anton Mitrofanov <BugMaster@narod.ru>
;*          Fiona Glaser <fiona@x264.com>
;*
;* Permission to use, copy, modify, and/or distribute this software for any
;* purpose with or without fee is hereby granted, provided that the above
;* copyright notice and this permission notice appear in all copies.
;*
;* THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
;* WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
;* MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
;* ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
;* WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
;* ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
;* OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
;*****************************************************************************

; This is a header file for the x86inc.asm assembly language, which uses
; NASM/YASM syntax combined with a large number of macros to provide easy
; abstraction between different calling conventions (x86_32, win64, linux64).
; It also has various other useful features to simplify writing the kind of
; DSP functions that are most often used.

%ifndef private_prefix
    %error private_prefix not defined
%endif

%ifndef public_prefix
    %define public_prefix private_prefix
%endif

%ifndef STACK_ALIGNMENT
    %if ARCH_X86_64
        %define STACK_ALIGNMENT 16
    %else
        %define STACK_ALIGNMENT 4
    %endif
%endif

%define WIN32  0
%define WIN64  0
%define UNIX64 0
%if ARCH_X86_64
    %ifidn __OUTPUT_FORMAT__,win32
        %define WIN32  1
        %define WIN64  1
    %elifidn __OUTPUT_FORMAT__,win64
        %define WIN32  1
        %define WIN64  1
    %elifidn __OUTPUT_FORMAT__,x64
        %define WIN32  1
        %define WIN64  1
    %else
        %define UNIX64 1
    %endif
%else
    %ifidn __OUTPUT_FORMAT__,win32
        %define WIN32  1
    %endif
%endif

%define FORMAT_ELF 0
%define FORMAT_MACHO 0
%ifidn __OUTPUT_FORMAT__,elf
    %define FORMAT_ELF 1
%elifidn __OUTPUT_FORMAT__,elf32
    %define FORMAT_ELF 1
%elifidn __OUTPUT_FORMAT__,elf64
    %define FORMAT_ELF 1
%elifidn __OUTPUT_FORMAT__,macho
    %define FORMAT_MACHO 1
%elifidn __OUTPUT_FORMAT__,macho32
    %define FORMAT_MACHO 1
%elifidn __OUTPUT_FORMAT__,macho64
    %define FORMAT_MACHO 1
%endif

%ifdef PREFIX
    %define mangle(x) _ %+ x
%else
    %define mangle(x) x
%endif

; Use VEX-encoding even in non-AVX functions
%ifndef FORCE_VEX_ENCODING
    %define FORCE_VEX_ENCODING 0
%endif

%macro SECTION_RODATA 0-1 16
    %ifidn __OUTPUT_FORMAT__,win32
        SECTION .rdata align=%1
    %elif WIN64
        SECTION .rdata align=%1
    %else
        SECTION .rodata align=%1
    %endif
%endmacro

%if ARCH_X86_64
    %define PIC 1 ; always use PIC on x86-64
    default rel
%elifidn __OUTPUT_FORMAT__,win32
    %define PIC 0 ; PIC isn't used on 32-bit Windows
%elifndef PIC
    %define PIC 0
%endif

%define HAVE_PRIVATE_EXTERN 1
%ifdef __NASM_VERSION_ID__
    %use smartalign
    %if __NASM_VERSION_ID__ < 0x020e0000 ; 2.14
        %define HAVE_PRIVATE_EXTERN 0
    %endif
%endif

; Macros to eliminate most code duplication between x86_32 and x86_64:
; Currently this works only for leaf functions which load all their arguments
; into registers at the start, and make no other use of the stack. Luckily that
; covers most use cases.

; PROLOGUE:
; %1 = number of arguments. loads them from stack if needed.
; %2 = number of registers used. pushes callee-saved regs if needed.
; %3 = number of xmm registers used. pushes callee-saved xmm regs if needed.
; %4 = (optional) stack size to be allocated. The stack will be aligned before
;      allocating the specified stack size. If the required stack alignment is
;      larger than the known stack alignment the stack will be manually aligned
;      and an extra register will be allocated to hold the original stack
;      pointer (to not invalidate r0m etc.). To prevent the use of an extra
;      register as stack pointer, request a negative stack size.
; %4+/%5+ = list of names to define to registers
; PROLOGUE can also be invoked by adding the same options to cglobal

; e.g.
; cglobal foo, 2,3,7,0x40, dst, src, tmp
; declares a function (foo) that automatically loads two arguments (dst and
; src) into registers, uses one additional register (tmp) plus 7 vector
; registers (m0-m6) and allocates 0x40 bytes of stack space.

; TODO Some functions can use some args directly from the stack. If they're the
; last args then you can just not declare them, but if they're in the middle
; we need more flexible macro.

; RET:
; Pops anything that was pushed by PROLOGUE, and returns.

; REP_RET:
; Use this instead of RET if it's a branch target.

; registers:
; rN and rNq are the native-size register holding function argument N
; rNd, rNw, rNb are dword, word, and byte size
; rNh is the high 8 bits of the word size
; rNm is the original location of arg N (a register or on the stack), dword
; rNmp is native size

%macro DECLARE_REG 2-3
    %define r%1q %2
    %define r%1d %2d
    %define r%1w %2w
    %define r%1b %2b
    %define r%1h %2h
    %define %2q %2
    %if %0 == 2
        %define r%1m  %2d
        %define r%1mp %2
    %elif ARCH_X86_64 ; memory
        %define r%1m [rstk + stack_offset + %3]
        %define r%1mp qword r %+ %1 %+ m
    %else
        %define r%1m [rstk + stack_offset + %3]
        %define r%1mp dword r %+ %1 %+ m
    %endif
    %define r%1  %2
%endmacro

%macro DECLARE_REG_SIZE 3
    %define r%1q r%1
    %define e%1q r%1
    %define r%1d e%1
    %define e%1d e%1
    %define r%1w %1
    %define e%1w %1
    %define r%1h %3
    %define e%1h %3
    %define r%1b %2
    %define e%1b %2
    %if ARCH_X86_64 == 0
        %define r%1 e%1
    %endif
%endmacro

DECLARE_REG_SIZE ax, al, ah
DECLARE_REG_SIZE bx, bl, bh
DECLARE_REG_SIZE cx, cl, ch
DECLARE_REG_SIZE dx, dl, dh
DECLARE_REG_SIZE si, sil, null
DECLARE_REG_SIZE di, dil, null
DECLARE_REG_SIZE bp, bpl, null

; t# defines for when per-arch register allocation is more complex than just function arguments

%macro DECLARE_REG_TMP 1-*
    %assign %%i 0
    %rep %0
        CAT_XDEFINE t, %%i, r%1
        %assign %%i %%i+1
        %rotate 1
    %endrep
%endmacro

%macro DECLARE_REG_TMP_SIZE 0-*
    %rep %0
        %define t%1q t%1 %+ q
        %define t%1d t%1 %+ d
        %define t%1w t%1 %+ w
        %define t%1h t%1 %+ h
        %define t%1b t%1 %+ b
        %rotate 1
    %endrep
%endmacro

DECLARE_REG_TMP_SIZE 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14

%if ARCH_X86_64
    %define gprsize 8
%else
    %define gprsize 4
%endif

%macro LEA 2
%if ARCH_X86_64
    lea %1, [%2]
%elif PIC
    call $+5 ; special-cased to not affect the RSB on most CPU:s
    pop %1
    add %1, -$+1+%2
%else
    mov %1, %2
%endif
%endmacro

; Repeats an instruction/operation for multiple arguments.
; Example usage: "REPX {psrlw x, 8}, m0, m1, m2, m3"
%macro REPX 2-* ; operation, args
    %xdefine %%f(x) %1
    %rep %0 - 1
        %rotate 1
        %%f(%1)
    %endrep
%endmacro

%macro PUSH 1
    push %1
    %ifidn rstk, rsp
        %assign stack_offset stack_offset+gprsize
    %endif
%endmacro

%macro POP 1
    pop %1
    %ifidn rstk, rsp
        %assign stack_offset stack_offset-gprsize
    %endif
%endmacro

%macro PUSH_IF_USED 1-*
    %rep %0
        %if %1 < regs_used
            PUSH r%1
        %endif
        %rotate 1
    %endrep
%endmacro

%macro POP_IF_USED 1-*
    %rep %0
        %if %1 < regs_used
            pop r%1
        %endif
        %rotate 1
    %endrep
%endmacro

%macro LOAD_IF_USED 1-*
    %rep %0
        %if %1 < num_args
            mov r%1, r %+ %1 %+ mp
        %endif
        %rotate 1
    %endrep
%endmacro

%macro SUB 2
    sub %1, %2
    %ifidn %1, rstk
        %assign stack_offset stack_offset+(%2)
    %endif
%endmacro

%macro ADD 2
    add %1, %2
    %ifidn %1, rstk
        %assign stack_offset stack_offset-(%2)
    %endif
%endmacro

%macro movifnidn 2
    %ifnidn %1, %2
        mov %1, %2
    %endif
%endmacro

%if ARCH_X86_64 == 0
    %define movsxd movifnidn
%endif

%macro movsxdifnidn 2
    %ifnidn %1, %2
        movsxd %1, %2
    %endif
%endmacro

%macro ASSERT 1
    %if (%1) == 0
        %error assertion ``%1'' failed
    %endif
%endmacro

%macro DEFINE_ARGS 0-*
    %ifdef n_arg_names
        %assign %%i 0
        %rep n_arg_names
            CAT_UNDEF arg_name %+ %%i, q
            CAT_UNDEF arg_name %+ %%i, d
            CAT_UNDEF arg_name %+ %%i, w
            CAT_UNDEF arg_name %+ %%i, h
            CAT_UNDEF arg_name %+ %%i, b
            CAT_UNDEF arg_name %+ %%i, m
            CAT_UNDEF arg_name %+ %%i, mp
            CAT_UNDEF arg_name, %%i
            %assign %%i %%i+1
        %endrep
    %endif

    %xdefine %%stack_offset stack_offset
    %undef stack_offset ; so that the current value of stack_offset doesn't get baked in by xdefine
    %assign %%i 0
    %rep %0
        %xdefine %1q r %+ %%i %+ q
        %xdefine %1d r %+ %%i %+ d
        %xdefine %1w r %+ %%i %+ w
        %xdefine %1h r %+ %%i %+ h
        %xdefine %1b r %+ %%i %+ b
        %xdefine %1m r %+ %%i %+ m
        %xdefine %1mp r %+ %%i %+ mp
        CAT_XDEFINE arg_name, %%i, %1
        %assign %%i %%i+1
        %rotate 1
    %endrep
    %xdefine stack_offset %%stack_offset
    %assign n_arg_names %0
%endmacro

%define required_stack_alignment ((mmsize + 15) & ~15)
%define vzeroupper_required (mmsize > 16 && (ARCH_X86_64 == 0 || xmm_regs_used > 16 || notcpuflag(avx512)))
%define high_mm_regs (16*cpuflag(avx512))

; Large stack allocations on Windows need to use stack probing in order
; to guarantee that all stack memory is committed before accessing it.
; This is done by ensuring that the guard page(s) at the end of the
; currently committed pages are touched prior to any pages beyond that.
%if WIN64
    %assign STACK_PROBE_SIZE 8192
%elifidn __OUTPUT_FORMAT__, win32
    %assign STACK_PROBE_SIZE 4096
%else
    %assign STACK_PROBE_SIZE 0
%endif

%macro PROBE_STACK 1 ; stack_size
    %if STACK_PROBE_SIZE
        %assign %%i STACK_PROBE_SIZE
        %rep %1 / STACK_PROBE_SIZE
            mov eax, [rsp-%%i]
            %assign %%i %%i+STACK_PROBE_SIZE
        %endrep
    %endif
%endmacro

%macro RESET_STACK_STATE 0
    %ifidn rstk, rsp
        %assign stack_offset stack_offset - stack_size_padded
    %else
        %xdefine rstk rsp
    %endif
    %assign stack_size 0
    %assign stack_size_padded 0
    %assign xmm_regs_used 0
%endmacro

%macro ALLOC_STACK 0-2 0, 0 ; stack_size, n_xmm_regs
    RESET_STACK_STATE
    %ifnum %2
        %if mmsize != 8
            %assign xmm_regs_used %2
        %endif
    %endif
    %ifnum %1
        %if %1 != 0
            %assign %%pad 0
            %assign stack_size %1
            %if stack_size < 0
                %assign stack_size -stack_size
            %endif
            %if WIN64
                %assign %%pad %%pad + 32 ; shadow space
                %if xmm_regs_used > 8
                    %assign %%pad %%pad + (xmm_regs_used-8)*16 ; callee-saved xmm registers
                %endif
            %endif
            %if required_stack_alignment <= STACK_ALIGNMENT
                ; maintain the current stack alignment
                %assign stack_size_padded stack_size + %%pad + ((-%%pad-stack_offset-gprsize) & (STACK_ALIGNMENT-1))
                PROBE_STACK stack_size_padded
                SUB rsp, stack_size_padded
            %else
                %assign %%reg_num (regs_used - 1)
                %xdefine rstk r %+ %%reg_num
                ; align stack, and save original stack location directly above
                ; it, i.e. in [rsp+stack_size_padded], so we can restore the
                ; stack in a single instruction (i.e. mov rsp, rstk or mov
                ; rsp, [rsp+stack_size_padded])
                %if %1 < 0 ; need to store rsp on stack
                    %xdefine rstkm [rsp + stack_size + %%pad]
                    %assign %%pad %%pad + gprsize
                %else ; can keep rsp in rstk during whole function
                    %xdefine rstkm rstk
                %endif
                %assign stack_size_padded stack_size + ((%%pad + required_stack_alignment-1) & ~(required_stack_alignment-1))
                PROBE_STACK stack_size_padded
                mov rstk, rsp
                and rsp, ~(required_stack_alignment-1)
                sub rsp, stack_size_padded
                movifnidn rstkm, rstk
            %endif
            WIN64_PUSH_XMM
        %endif
    %endif
%endmacro

%macro SETUP_STACK_POINTER 0-1 0
    %ifnum %1
        %if %1 != 0 && required_stack_alignment > STACK_ALIGNMENT
            %if %1 > 0
                ; Reserve an additional register for storing the original stack pointer, but avoid using
                ; eax/rax for this purpose since it can potentially get overwritten as a return value.
                %assign regs_used (regs_used + 1)
                %if ARCH_X86_64 && regs_used == 7
                    %assign regs_used 8
                %elif ARCH_X86_64 == 0 && regs_used == 1
                    %assign regs_used 2
                %endif
            %endif
            %if ARCH_X86_64 && regs_used < 5 + UNIX64 * 3
                ; Ensure that we don't clobber any registers containing arguments. For UNIX64 we also preserve r6 (rax)
                ; since it's used as a hidden argument in vararg functions to specify the number of vector registers used.
                %assign regs_used 5 + UNIX64 * 3
            %endif
        %endif
    %endif
%endmacro

%if WIN64 ; Windows x64 ;=================================================

DECLARE_REG 0,  rcx
DECLARE_REG 1,  rdx
DECLARE_REG 2,  R8
DECLARE_REG 3,  R9
DECLARE_REG 4,  R10, 40
DECLARE_REG 5,  R11, 48
DECLARE_REG 6,  rax, 56
DECLARE_REG 7,  rdi, 64
DECLARE_REG 8,  rsi, 72
DECLARE_REG 9,  rbx, 80
DECLARE_REG 10, rbp, 88
DECLARE_REG 11, R14, 96
DECLARE_REG 12, R15, 104
DECLARE_REG 13, R12, 112
DECLARE_REG 14, R13, 120

%macro PROLOGUE 2-5+ 0, 0 ; #args, #regs, #xmm_regs, [stack_size,] arg_names...
    %assign num_args %1
    %assign regs_used %2
    ASSERT regs_used >= num_args
    SETUP_STACK_POINTER %4
    ASSERT regs_used <= 15
    PUSH_IF_USED 7, 8, 9, 10, 11, 12, 13, 14
    ALLOC_STACK %4, %3
    %if mmsize != 8 && stack_size == 0
        WIN64_SPILL_XMM %3
    %endif
    LOAD_IF_USED 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
    %if %0 > 4
        %ifnum %4
            DEFINE_ARGS %5
        %else
            DEFINE_ARGS %4, %5
        %endif
    %elifnnum %4
        DEFINE_ARGS %4
    %endif
%endmacro

; Push XMM registers to the stack. If no argument is specified all used register
; will be pushed, otherwise only push previously unpushed registers.
%macro WIN64_PUSH_XMM 0-2 ; new_xmm_regs_used, xmm_regs_pushed
    %if mmsize != 8
        %if %0 == 2
            %assign %%pushed %2
            %assign xmm_regs_used %1
        %elif %0 == 1
            %assign %%pushed xmm_regs_used
            %assign xmm_regs_used %1
        %else
            %assign %%pushed 0
        %endif
        ; Use the shadow space to store XMM6 and XMM7, the rest needs stack space allocated.
        %if %%pushed <= 6 + high_mm_regs && xmm_regs_used > 6 + high_mm_regs
            movaps [rstk + stack_offset +  8], xmm6
        %endif
        %if %%pushed <= 7 + high_mm_regs && xmm_regs_used > 7 + high_mm_regs
            movaps [rstk + stack_offset + 24], xmm7
        %endif
        %assign %%pushed %%pushed - high_mm_regs - 8
        %if %%pushed < 0
            %assign %%pushed 0
        %endif
        %assign %%regs_to_push xmm_regs_used - %%pushed - high_mm_regs - 8
        %if %%regs_to_push > 0
            ASSERT (%%regs_to_push + %%pushed) * 16 <= stack_size_padded - stack_size - 32
            %assign %%i %%pushed + 8
            %rep %%regs_to_push
                movaps [rsp + (%%i-8)*16 + stack_size + 32], xmm %+ %%i
                %assign %%i %%i+1
            %endrep
        %endif
    %endif
%endmacro

; Allocated stack space for XMM registers and push all, or a subset, of those
%macro WIN64_SPILL_XMM 1-2 ; xmm_regs_used, xmm_regs_reserved
    RESET_STACK_STATE
    %if mmsize != 8
        %assign xmm_regs_used %1
        ASSERT xmm_regs_used <= 16 + high_mm_regs
        %if %0 == 2
            ASSERT %2 >= %1
            %assign %%xmm_regs_on_stack %2 - high_mm_regs - 8
        %else
            %assign %%xmm_regs_on_stack %1 - high_mm_regs - 8
        %endif
        %if %%xmm_regs_on_stack > 0
            ; Allocate stack space for callee-saved xmm registers plus shadow space and align the stack.
            %assign %%pad %%xmm_regs_on_stack*16 + 32
            %assign stack_size_padded %%pad + ((-%%pad-stack_offset-gprsize) & (STACK_ALIGNMENT-1))
            SUB rsp, stack_size_padded
        %endif
        WIN64_PUSH_XMM
    %endif
%endmacro

%macro WIN64_RESTORE_XMM_INTERNAL 0
    %assign %%pad_size 0
    %assign %%xmm_regs_on_stack xmm_regs_used - high_mm_regs - 8
    %if %%xmm_regs_on_stack > 0
        %assign %%i xmm_regs_used - high_mm_regs
        %rep %%xmm_regs_on_stack
            %assign %%i %%i-1
            movaps xmm %+ %%i, [rsp + (%%i-8)*16 + stack_size + 32]
        %endrep
    %endif
    %if stack_size_padded > 0
        %if stack_size > 0 && required_stack_alignment > STACK_ALIGNMENT
            mov rsp, rstkm
        %else
            add rsp, stack_size_padded
            %assign %%pad_size stack_size_padded
        %endif
    %endif
    %if xmm_regs_used > 7 + high_mm_regs
        movaps xmm7, [rsp + stack_offset - %%pad_size + 24]
    %endif
    %if xmm_regs_used > 6 + high_mm_regs
        movaps xmm6, [rsp + stack_offset - %%pad_size +  8]
    %endif
%endmacro

%macro WIN64_RESTORE_XMM 0
    WIN64_RESTORE_XMM_INTERNAL
    RESET_STACK_STATE
%endmacro

%define has_epilogue regs_used > 7 || stack_size > 0 || vzeroupper_required || xmm_regs_used > 6+high_mm_regs

%macro RET 0
    WIN64_RESTORE_XMM_INTERNAL
    POP_IF_USED 14, 13, 12, 11, 10, 9, 8, 7
    %if vzeroupper_required
        vzeroupper
    %endif
    AUTO_REP_RET
%endmacro

%elif ARCH_X86_64 ; *nix x64 ;=============================================

DECLARE_REG 0,  rdi
DECLARE_REG 1,  rsi
DECLARE_REG 2,  rdx
DECLARE_REG 3,  rcx
DECLARE_REG 4,  R8
DECLARE_REG 5,  R9
DECLARE_REG 6,  rax, 8
DECLARE_REG 7,  R10, 16
DECLARE_REG 8,  R11, 24
DECLARE_REG 9,  rbx, 32
DECLARE_REG 10, rbp, 40
DECLARE_REG 11, R14, 48
DECLARE_REG 12, R15, 56
DECLARE_REG 13, R12, 64
DECLARE_REG 14, R13, 72

%macro PROLOGUE 2-5+ 0, 0 ; #args, #regs, #xmm_regs, [stack_size,] arg_names...
    %assign num_args %1
    %assign regs_used %2
    ASSERT regs_used >= num_args
    SETUP_STACK_POINTER %4
    ASSERT regs_used <= 15
    PUSH_IF_USED 9, 10, 11, 12, 13, 14
    ALLOC_STACK %4, %3
    LOAD_IF_USED 6, 7, 8, 9, 10, 11, 12, 13, 14
    %if %0 > 4
        %ifnum %4
            DEFINE_ARGS %5
        %else
            DEFINE_ARGS %4, %5
        %endif
    %elifnnum %4
        DEFINE_ARGS %4
    %endif
%endmacro

%define has_epilogue regs_used > 9 || stack_size > 0 || vzeroupper_required

%macro RET 0
    %if stack_size_padded > 0
        %if required_stack_alignment > STACK_ALIGNMENT
            mov rsp, rstkm
        %else
            add rsp, stack_size_padded
        %endif
    %endif
    POP_IF_USED 14, 13, 12, 11, 10, 9
    %if vzeroupper_required
        vzeroupper
    %endif
    AUTO_REP_RET
%endmacro

%else ; X86_32 ;==============================================================

DECLARE_REG 0, eax, 4
DECLARE_REG 1, ecx, 8
DECLARE_REG 2, edx, 12
DECLARE_REG 3, ebx, 16
DECLARE_REG 4, esi, 20
DECLARE_REG 5, edi, 24
DECLARE_REG 6, ebp, 28
%define rsp esp

%macro DECLARE_ARG 1-*
    %rep %0
        %define r%1m [rstk + stack_offset + 4*%1 + 4]
        %define r%1mp dword r%1m
        %rotate 1
    %endrep
%endmacro

DECLARE_ARG 7, 8, 9, 10, 11, 12, 13, 14

%macro PROLOGUE 2-5+ 0, 0 ; #args, #regs, #xmm_regs, [stack_size,] arg_names...
    %assign num_args %1
    %assign regs_used %2
    ASSERT regs_used >= num_args
    %if num_args > 7
        %assign num_args 7
    %endif
    %if regs_used > 7
        %assign regs_used 7
    %endif
    SETUP_STACK_POINTER %4
    ASSERT regs_used <= 7
    PUSH_IF_USED 3, 4, 5, 6
    ALLOC_STACK %4, %3
    LOAD_IF_USED 0, 1, 2, 3, 4, 5, 6
    %if %0 > 4
        %ifnum %4
            DEFINE_ARGS %5
        %else
            DEFINE_ARGS %4, %5
        %endif
    %elifnnum %4
        DEFINE_ARGS %4
    %endif
%endmacro

%define has_epilogue regs_used > 3 || stack_size > 0 || vzeroupper_required

%macro RET 0
    %if stack_size_padded > 0
        %if required_stack_alignment > STACK_ALIGNMENT
            mov rsp, rstkm
        %else
            add rsp, stack_size_padded
        %endif
    %endif
    POP_IF_USED 6, 5, 4, 3
    %if vzeroupper_required
        vzeroupper
    %endif
    AUTO_REP_RET
%endmacro

%endif ;======================================================================

%if WIN64 == 0
    %macro WIN64_SPILL_XMM 1-2
        RESET_STACK_STATE
        %if mmsize != 8
            %assign xmm_regs_used %1
        %endif
    %endmacro
    %macro WIN64_RESTORE_XMM 0
        RESET_STACK_STATE
    %endmacro
    %macro WIN64_PUSH_XMM 0-2
        %if mmsize != 8 && %0 >= 1
            %assign xmm_regs_used %1
        %endif
    %endmacro
%endif

; On AMD cpus <=K10, an ordinary ret is slow if it immediately follows either
; a branch or a branch target. So switch to a 2-byte form of ret in that case.
; We can automatically detect "follows a branch", but not a branch target.
; (SSSE3 is a sufficient condition to know that your cpu doesn't have this problem.)
%macro REP_RET 0
    %if has_epilogue || cpuflag(ssse3)
        RET
    %else
        rep ret
    %endif
    annotate_function_size
%endmacro

%define last_branch_adr $$
%macro AUTO_REP_RET 0
    %if notcpuflag(ssse3)
        times ((last_branch_adr-$)>>31)+1 rep ; times 1 iff $ == last_branch_adr.
    %endif
    ret
    annotate_function_size
%endmacro

%macro BRANCH_INSTR 0-*
    %rep %0
        %macro %1 1-2 %1
            %2 %1
            %if notcpuflag(ssse3)
                %%branch_instr equ $
                %xdefine last_branch_adr %%branch_instr
            %endif
        %endmacro
        %rotate 1
    %endrep
%endmacro

BRANCH_INSTR jz, je, jnz, jne, jl, jle, jnl, jnle, jg, jge, jng, jnge, ja, jae, jna, jnae, jb, jbe, jnb, jnbe, jc, jnc, js, jns, jo, jno, jp, jnp

%macro TAIL_CALL 1-2 1 ; callee, is_nonadjacent
    %if has_epilogue
        call %1
        RET
    %elif %2
        jmp %1
    %endif
    annotate_function_size
%endmacro

;=============================================================================
; arch-independent part
;=============================================================================

%assign function_align 16

; Begin a function.
; Applies any symbol mangling needed for C linkage, and sets up a define such that
; subsequent uses of the function name automatically refer to the mangled version.
; Appends cpuflags to the function name if cpuflags has been specified.
; The "" empty default parameter is a workaround for nasm, which fails if SUFFIX
; is empty and we call cglobal_internal with just %1 %+ SUFFIX (without %2).
%macro cglobal 1-2+ "" ; name, [PROLOGUE args]
    cglobal_internal 1, %1 %+ SUFFIX, %2
%endmacro
%macro cvisible 1-2+ "" ; name, [PROLOGUE args]
    cglobal_internal 0, %1 %+ SUFFIX, %2
%endmacro
%macro cglobal_internal 2-3+
    annotate_function_size
    %ifndef cglobaled_%2
        %if %1
            %xdefine %2 mangle(private_prefix %+ _ %+ %2)
        %else
            %xdefine %2 mangle(public_prefix %+ _ %+ %2)
        %endif
        %xdefine %2.skip_prologue %2 %+ .skip_prologue
        CAT_XDEFINE cglobaled_, %2, 1
    %endif
    %xdefine current_function %2
    %xdefine current_function_section __SECT__
    %if FORMAT_ELF
        %if %1
            global %2:function hidden
        %else
            global %2:function
        %endif
    %elif FORMAT_MACHO && HAVE_PRIVATE_EXTERN && %1
        global %2:private_extern
    %else
        global %2
    %endif
    %if WIN32 && !%1
        %ifdef BUILDING_DLL
            export %2
        %endif
    %endif
    align function_align
    %2:
    RESET_MM_PERMUTATION        ; needed for x86-64, also makes disassembly somewhat nicer
    %xdefine rstk rsp           ; copy of the original stack pointer, used when greater alignment than the known stack alignment is required
    %assign stack_offset 0      ; stack pointer offset relative to the return address
    %assign stack_size 0        ; amount of stack space that can be freely used inside a function
    %assign stack_size_padded 0 ; total amount of allocated stack space, including space for callee-saved xmm registers on WIN64 and alignment padding
    %assign xmm_regs_used 0     ; number of XMM registers requested, used for dealing with callee-saved registers on WIN64 and vzeroupper
    %ifnidn %3, ""
        PROLOGUE %3
    %endif
%endmacro

; Create a global symbol from a local label with the correct name mangling and type
%macro cglobal_label 1
    %if FORMAT_ELF
        global current_function %+ %1:function hidden
    %elif FORMAT_MACHO && HAVE_PRIVATE_EXTERN
        global current_function %+ %1:private_extern
    %else
        global current_function %+ %1
    %endif
    %1:
%endmacro

%macro cextern 1
    %xdefine %1 mangle(private_prefix %+ _ %+ %1)
    CAT_XDEFINE cglobaled_, %1, 2
    extern %1
%endmacro

; Like cextern, but without the prefix. This should be used for symbols from external libraries.
%macro cextern_naked 1
    %ifdef PREFIX
        %xdefine %1 mangle(%1)
    %endif
    CAT_XDEFINE cglobaled_, %1, 3
    extern %1
%endmacro

%macro const 1-2+
    %xdefine %1 mangle(private_prefix %+ _ %+ %1)
    %if FORMAT_ELF
        global %1:data hidden
    %elif FORMAT_MACHO && HAVE_PRIVATE_EXTERN
        global %1:private_extern
    %else
        global %1
    %endif
    %1: %2
%endmacro

%if FORMAT_ELF
    ; The GNU linker assumes the stack is executable by default.
    [SECTION .note.GNU-stack noalloc noexec nowrite progbits]

    %ifdef __NASM_VERSION_ID__
        %if __NASM_VERSION_ID__ >= 0x020e0300 ; 2.14.03
            %if ARCH_X86_64
                ; Control-flow Enforcement Technology (CET) properties.
                [SECTION .note.gnu.property alloc noexec nowrite note align=gprsize]
                dd 0x00000004  ; n_namesz
                dd gprsize + 8 ; n_descsz
                dd 0x00000005  ; n_type = NT_GNU_PROPERTY_TYPE_0
                db "GNU",0     ; n_name
                dd 0xc0000002  ; pr_type = GNU_PROPERTY_X86_FEATURE_1_AND
                dd 0x00000004  ; pr_datasz
                dd 0x00000002  ; pr_data = GNU_PROPERTY_X86_FEATURE_1_SHSTK
                dd 0x00000000  ; pr_padding
            %endif
        %endif
    %endif
%endif

; Tell debuggers how large the function was.
; This may be invoked multiple times per function; we rely on later instances overriding earlier ones.
; This is invoked by RET and similar macros, and also cglobal does it for the previous function,
; but if the last function in a source file doesn't use any of the standard macros for its epilogue,
; then its size might be unspecified.
%macro annotate_function_size 0
    %ifdef __YASM_VER__
        %ifdef current_function
            %if FORMAT_ELF
                current_function_section
                %%ecf equ $
                size current_function %%ecf - current_function
                __SECT__
            %endif
        %endif
    %endif
%endmacro

; cpuflags

%assign cpuflags_mmx       (1<<0)
%assign cpuflags_mmx2      (1<<1)  | cpuflags_mmx
%assign cpuflags_3dnow     (1<<2)  | cpuflags_mmx
%assign cpuflags_3dnowext  (1<<3)  | cpuflags_3dnow
%assign cpuflags_sse       (1<<4)  | cpuflags_mmx2
%assign cpuflags_sse2      (1<<5)  | cpuflags_sse
%assign cpuflags_sse2slow  (1<<6)  | cpuflags_sse2
%assign cpuflags_lzcnt     (1<<7)  | cpuflags_sse2
%assign cpuflags_sse3      (1<<8)  | cpuflags_sse2
%assign cpuflags_ssse3     (1<<9)  | cpuflags_sse3
%assign cpuflags_sse4      (1<<10) | cpuflags_ssse3
%assign cpuflags_sse42     (1<<11) | cpuflags_sse4
%assign cpuflags_aesni     (1<<12) | cpuflags_sse42
%assign cpuflags_clmul     (1<<13) | cpuflags_sse42
%assign cpuflags_gfni      (1<<14) | cpuflags_aesni|cpuflags_clmul
%assign cpuflags_avx       (1<<15) | cpuflags_sse42
%assign cpuflags_xop       (1<<16) | cpuflags_avx
%assign cpuflags_fma4      (1<<17) | cpuflags_avx
%assign cpuflags_fma3      (1<<18) | cpuflags_avx
%assign cpuflags_bmi1      (1<<19) | cpuflags_avx|cpuflags_lzcnt
%assign cpuflags_bmi2      (1<<20) | cpuflags_bmi1
%assign cpuflags_avx2      (1<<21) | cpuflags_fma3|cpuflags_bmi2
%assign cpuflags_avx512    (1<<22) | cpuflags_avx2 ; F, CD, BW, DQ, VL
%assign cpuflags_avx512icl (1<<23) | cpuflags_avx512|cpuflags_gfni ; VNNI, IFMA, VBMI, VBMI2, VPOPCNTDQ, BITALG, VAES, VPCLMULQDQ

%assign cpuflags_cache32   (1<<24)
%assign cpuflags_cache64   (1<<25)
%assign cpuflags_aligned   (1<<26) ; not a cpu feature, but a function variant
%assign cpuflags_atom      (1<<27)

; Returns a boolean value expressing whether or not the specified cpuflag is enabled.
%define    cpuflag(x) (((((cpuflags & (cpuflags_ %+ x)) ^ (cpuflags_ %+ x)) - 1) >> 31) & 1)
%define notcpuflag(x) (cpuflag(x) ^ 1)

; Takes an arbitrary number of cpuflags from the above list.
; All subsequent functions (up to the next INIT_CPUFLAGS) is built for the specified cpu.
; You shouldn't need to invoke this macro directly, it's a subroutine for INIT_MMX &co.
%macro INIT_CPUFLAGS 0-*
    %xdefine SUFFIX
    %undef cpuname
    %assign cpuflags 0

    %if %0 >= 1
        %rep %0
            %ifdef cpuname
                %xdefine cpuname cpuname %+ _%1
            %else
                %xdefine cpuname %1
            %endif
            %assign cpuflags cpuflags | cpuflags_%1
            %rotate 1
        %endrep
        %xdefine SUFFIX _ %+ cpuname

        %if cpuflag(avx)
            %assign avx_enabled 1
        %endif
        %if (mmsize == 16 && notcpuflag(sse2)) || (mmsize == 32 && notcpuflag(avx2))
            %define mova movaps
            %define movu movups
            %define movnta movntps
        %endif
        %if cpuflag(aligned)
            %define movu mova
        %elif cpuflag(sse3) && notcpuflag(ssse3)
            %define movu lddqu
        %endif
    %endif

    %if ARCH_X86_64 || cpuflag(sse2)
        %ifdef __NASM_VERSION_ID__
            ALIGNMODE p6
        %else
            CPU amdnop
        %endif
    %else
        %ifdef __NASM_VERSION_ID__
            ALIGNMODE nop
        %else
            CPU basicnop
        %endif
    %endif
%endmacro

; Merge mmx, sse*, and avx*
; m# is a simd register of the currently selected size
; xm# is the corresponding xmm register if mmsize >= 16, otherwise the same as m#
; ym# is the corresponding ymm register if mmsize >= 32, otherwise the same as m#
; zm# is the corresponding zmm register if mmsize >= 64, otherwise the same as m#
; (All 4 remain in sync through SWAP.)

%macro CAT_XDEFINE 3
    %xdefine %1%2 %3
%endmacro

%macro CAT_UNDEF 2
    %undef %1%2
%endmacro

%macro DEFINE_MMREGS 1 ; mmtype
    %assign %%prev_mmregs 0
    %ifdef num_mmregs
        %assign %%prev_mmregs num_mmregs
    %endif

    %assign num_mmregs 8
    %if ARCH_X86_64 && mmsize >= 16
        %assign num_mmregs 16
        %if cpuflag(avx512) || mmsize == 64
            %assign num_mmregs 32
        %endif
    %endif

    %assign %%i 0
    %rep num_mmregs
        CAT_XDEFINE m, %%i, %1 %+ %%i
        CAT_XDEFINE nn%1, %%i, %%i
        %assign %%i %%i+1
    %endrep
    %if %%prev_mmregs > num_mmregs
        %rep %%prev_mmregs - num_mmregs
            CAT_UNDEF m, %%i
            CAT_UNDEF nn %+ mmtype, %%i
            %assign %%i %%i+1
        %endrep
    %endif
    %xdefine mmtype %1
%endmacro

; Prefer registers 16-31 over 0-15 to avoid having to use vzeroupper
%macro AVX512_MM_PERMUTATION 0-1 0 ; start_reg
    %if ARCH_X86_64 && cpuflag(avx512)
        %assign %%i %1
        %rep 16-%1
            %assign %%i_high %%i+16
            SWAP %%i, %%i_high
            %assign %%i %%i+1
        %endrep
    %endif
%endmacro

%macro INIT_MMX 0-1+
    %assign avx_enabled 0
    %define RESET_MM_PERMUTATION INIT_MMX %1
    %define mmsize 8
    %define mova movq
    %define movu movq
    %define movh movd
    %define movnta movntq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS mm
%endmacro

%macro INIT_XMM 0-1+
    %assign avx_enabled FORCE_VEX_ENCODING
    %define RESET_MM_PERMUTATION INIT_XMM %1
    %define mmsize 16
    %define mova movdqa
    %define movu movdqu
    %define movh movq
    %define movnta movntdq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS xmm
    %if WIN64
        AVX512_MM_PERMUTATION 6 ; Swap callee-saved registers with volatile registers
    %endif
    %xdefine bcstw 1to8
    %xdefine bcstd 1to4
    %xdefine bcstq 1to2
%endmacro

%macro INIT_YMM 0-1+
    %assign avx_enabled 1
    %define RESET_MM_PERMUTATION INIT_YMM %1
    %define mmsize 32
    %define mova movdqa
    %define movu movdqu
    %undef movh
    %define movnta movntdq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS ymm
    AVX512_MM_PERMUTATION
    %xdefine bcstw 1to16
    %xdefine bcstd 1to8
    %xdefine bcstq 1to4
%endmacro

%macro INIT_ZMM 0-1+
    %assign avx_enabled 1
    %define RESET_MM_PERMUTATION INIT_ZMM %1
    %define mmsize 64
    %define mova movdqa
    %define movu movdqu
    %undef movh
    %define movnta movntdq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS zmm
    AVX512_MM_PERMUTATION
    %xdefine bcstw 1to32
    %xdefine bcstd 1to16
    %xdefine bcstq 1to8
%endmacro

INIT_XMM

%macro DECLARE_MMCAST 1
    %define  mmmm%1   mm%1
    %define  mmxmm%1  mm%1
    %define  mmymm%1  mm%1
    %define  mmzmm%1  mm%1
    %define xmmmm%1   mm%1
    %define xmmxmm%1 xmm%1
    %define xmmymm%1 xmm%1
    %define xmmzmm%1 xmm%1
    %define ymmmm%1   mm%1
    %define ymmxmm%1 xmm%1
    %define ymmymm%1 ymm%1
    %define ymmzmm%1 ymm%1
    %define zmmmm%1   mm%1
    %define zmmxmm%1 xmm%1
    %define zmmymm%1 ymm%1
    %define zmmzmm%1 zmm%1
    %define xm%1 xmm %+ m%1
    %define ym%1 ymm %+ m%1
    %define zm%1 zmm %+ m%1
%endmacro

%assign i 0
%rep 32
    DECLARE_MMCAST i
    %assign i i+1
%endrep

; I often want to use macros that permute their arguments. e.g. there's no
; efficient way to implement butterfly or transpose or dct without swapping some
; arguments.
;
; I would like to not have to manually keep track of the permutations:
; If I insert a permutation in the middle of a function, it should automatically
; change everything that follows. For more complex macros I may also have multiple
; implementations, e.g. the SSE2 and SSSE3 versions may have different permutations.
;
; Hence these macros. Insert a PERMUTE or some SWAPs at the end of a macro that
; permutes its arguments. It's equivalent to exchanging the contents of the
; registers, except that this way you exchange the register names instead, so it
; doesn't cost any cycles.

%macro PERMUTE 2-* ; takes a list of pairs to swap
    %rep %0/2
        %xdefine %%tmp%2 m%2
        %rotate 2
    %endrep
    %rep %0/2
        %xdefine m%1 %%tmp%2
        CAT_XDEFINE nn, m%1, %1
        %rotate 2
    %endrep
%endmacro

%macro SWAP 2+ ; swaps a single chain (sometimes more concise than pairs)
    %ifnum %1 ; SWAP 0, 1, ...
        SWAP_INTERNAL_NUM %1, %2
    %else ; SWAP m0, m1, ...
        SWAP_INTERNAL_NAME %1, %2
    %endif
%endmacro

%macro SWAP_INTERNAL_NUM 2-*
    %rep %0-1
        %xdefine %%tmp m%1
        %xdefine m%1 m%2
        %xdefine m%2 %%tmp
        CAT_XDEFINE nn, m%1, %1
        CAT_XDEFINE nn, m%2, %2
        %rotate 1
    %endrep
%endmacro

%macro SWAP_INTERNAL_NAME 2-*
    %xdefine %%args nn %+ %1
    %rep %0-1
        %xdefine %%args %%args, nn %+ %2
        %rotate 1
    %endrep
    SWAP_INTERNAL_NUM %%args
%endmacro

; If SAVE_MM_PERMUTATION is placed at the end of a function, then any later
; calls to that function will automatically load the permutation, so values can
; be returned in mmregs.
%macro SAVE_MM_PERMUTATION 0-1
    %if %0
        %xdefine %%f %1_m
    %else
        %xdefine %%f current_function %+ _m
    %endif
    %assign %%i 0
    %rep num_mmregs
        %xdefine %%tmp m %+ %%i
        CAT_XDEFINE %%f, %%i, regnumof %+ %%tmp
        %assign %%i %%i+1
    %endrep
%endmacro

%macro LOAD_MM_PERMUTATION 0-1 ; name to load from
    %if %0
        %xdefine %%f %1_m
    %else
        %xdefine %%f current_function %+ _m
    %endif
    %xdefine %%tmp %%f %+ 0
    %ifnum %%tmp
        DEFINE_MMREGS mmtype
        %assign %%i 0
        %rep num_mmregs
            %xdefine %%tmp %%f %+ %%i
            CAT_XDEFINE %%m, %%i, m %+ %%tmp
            %assign %%i %%i+1
        %endrep
        %rep num_mmregs
            %assign %%i %%i-1
            CAT_XDEFINE m, %%i, %%m %+ %%i
            CAT_XDEFINE nn, m %+ %%i, %%i
        %endrep
    %endif
%endmacro

; Append cpuflags to the callee's name iff the appended name is known and the plain name isn't
%macro call 1
    %ifid %1
        call_internal %1 %+ SUFFIX, %1
    %else
        call %1
    %endif
%endmacro
%macro call_internal 2
    %xdefine %%i %2
    %define %%j %%i
    %ifndef cglobaled_%2
        %ifdef cglobaled_%1
            %xdefine %%i %1
        %endif
    %elif FORMAT_ELF
        %if ARCH_X86_64
            %if cglobaled_%2 >= 2
                ; Always emit PLT relocations when calling external functions,
                ; the linker will eliminate unnecessary PLT indirections anyway.
                %define %%j %%i wrt ..plt
            %endif
        %elif PIC && cglobaled_%2 == 3
            ; Go through the GOT for functions declared using cextern_naked with
            ; PIC, as such functions presumably exists in external libraries.
            extern _GLOBAL_OFFSET_TABLE_
            LEA eax, $$+_GLOBAL_OFFSET_TABLE_ wrt ..gotpc
            %define %%j [eax+%%i wrt ..got]
        %endif
    %endif
    call %%j
    LOAD_MM_PERMUTATION %%i
%endmacro

; Substitutions that reduce instruction size but are functionally equivalent
%macro add 2
    %ifnum %2
        %if %2==128
            sub %1, -128
        %else
            add %1, %2
        %endif
    %else
        add %1, %2
    %endif
%endmacro

%macro sub 2
    %ifnum %2
        %if %2==128
            add %1, -128
        %else
            sub %1, %2
        %endif
    %else
        sub %1, %2
    %endif
%endmacro

;=============================================================================
; AVX abstraction layer
;=============================================================================

%assign i 0
%rep 32
    %if i < 8
        CAT_XDEFINE sizeofmm, i, 8
        CAT_XDEFINE regnumofmm, i, i
    %endif
    CAT_XDEFINE sizeofxmm, i, 16
    CAT_XDEFINE sizeofymm, i, 32
    CAT_XDEFINE sizeofzmm, i, 64
    CAT_XDEFINE regnumofxmm, i, i
    CAT_XDEFINE regnumofymm, i, i
    CAT_XDEFINE regnumofzmm, i, i
    %assign i i+1
%endrep
%undef i

%macro CHECK_AVX_INSTR_EMU 3-*
    %xdefine %%opcode %1
    %xdefine %%dst %2
    %rep %0-2
        %ifidn %%dst, %3
            %error non-avx emulation of ``%%opcode'' is not supported
        %endif
        %rotate 1
    %endrep
%endmacro

;%1 == instruction
;%2 == minimal instruction set
;%3 == 1 if float, 0 if int
;%4 == 1 if 4-operand emulation, 0 if 3-operand emulation, 255 otherwise (no emulation)
;%5 == 1 if commutative (i.e. doesn't matter which src arg is which), 0 if not
;%6+: operands
%macro RUN_AVX_INSTR 6-9+
    %ifnum sizeof%7
        %assign __sizeofreg sizeof%7
    %elifnum sizeof%6
        %assign __sizeofreg sizeof%6
    %else
        %assign __sizeofreg mmsize
    %endif
    %assign __emulate_avx 0
    %if avx_enabled && __sizeofreg >= 16
        %xdefine __instr v%1
    %else
        %xdefine __instr %1
        %if %0 >= 8+%4
            %assign __emulate_avx 1
        %endif
    %endif
    %ifnidn %2, fnord
        %ifdef cpuname
            %if notcpuflag(%2)
                %error use of ``%1'' %2 instruction in cpuname function: current_function
            %elif %3 == 0 && __sizeofreg == 16 && notcpuflag(sse2)
                %error use of ``%1'' sse2 instruction in cpuname function: current_function
            %elif %3 == 0 && __sizeofreg == 32 && notcpuflag(avx2)
                %error use of ``%1'' avx2 instruction in cpuname function: current_function
            %elif __sizeofreg == 16 && notcpuflag(sse)
                %error use of ``%1'' sse instruction in cpuname function: current_function
            %elif __sizeofreg == 32 && notcpuflag(avx)
                %error use of ``%1'' avx instruction in cpuname function: current_function
            %elif __sizeofreg == 64 && notcpuflag(avx512)
                %error use of ``%1'' avx512 instruction in cpuname function: current_function
            %elifidn %1, pextrw ; special case because the base instruction is mmx2,
                %ifnid %6       ; but sse4 is required for memory operands
                    %if notcpuflag(sse4)
                        %error use of ``%1'' sse4 instruction in cpuname function: current_function
                    %endif
                %endif
            %endif
        %endif
    %endif

    %if __emulate_avx
        %xdefine __src1 %7
        %xdefine __src2 %8
        %if %5 && %4 == 0
            %ifnidn %6, %7
                %ifidn %6, %8
                    %xdefine __src1 %8
                    %xdefine __src2 %7
                %elifnnum sizeof%8
                    ; 3-operand AVX instructions with a memory arg can only have it in src2,
                    ; whereas SSE emulation prefers to have it in src1 (i.e. the mov).
                    ; So, if the instruction is commutative with a memory arg, swap them.
                    %xdefine __src1 %8
                    %xdefine __src2 %7
                %endif
            %endif
        %endif
        %ifnidn %6, __src1
            %if %0 >= 9
                CHECK_AVX_INSTR_EMU {%1 %6, %7, %8, %9}, %6, __src2, %9
            %else
                CHECK_AVX_INSTR_EMU {%1 %6, %7, %8}, %6, __src2
            %endif
            %if __sizeofreg == 8
                MOVQ %6, __src1
            %elif %3
                MOVAPS %6, __src1
            %else
                MOVDQA %6, __src1
            %endif
        %endif
        %if %0 >= 9
            %1 %6, __src2, %9
        %else
            %1 %6, __src2
        %endif
    %elif %0 >= 9
        %if avx_enabled && __sizeofreg >= 16 && %4 == 1
            %ifnnum regnumof%7
                %if %3
                    vmovaps %6, %7
                %else
                    vmovdqa %6, %7
                %endif
                __instr %6, %6, %8, %9
            %else
                __instr %6, %7, %8, %9
            %endif
        %else
            __instr %6, %7, %8, %9
        %endif
    %elif %0 == 8
        %if avx_enabled && __sizeofreg >= 16 && %4 == 0
            %xdefine __src1 %7
            %xdefine __src2 %8
            %if %5
                %ifnum regnumof%7
                    %ifnum regnumof%8
                        %if regnumof%7 < 8 && regnumof%8 >= 8 && regnumof%8 < 16 && sizeof%8 <= 32
                            ; Most VEX-encoded instructions require an additional byte to encode when
                            ; src2 is a high register (e.g. m8..15). If the instruction is commutative
                            ; we can swap src1 and src2 when doing so reduces the instruction length.
                            %xdefine __src1 %8
                            %xdefine __src2 %7
                        %endif
                    %endif
                %elifnum regnumof%8 ; put memory operands in src2 when possible
                    %xdefine __src1 %8
                    %xdefine __src2 %7
                %else
                    %assign __emulate_avx 1
                %endif
            %elifnnum regnumof%7
                ; EVEX allows imm8 shift instructions to be used with memory operands,
                ; but VEX does not. This handles those special cases.
                %ifnnum %8
                    %assign __emulate_avx 1
                %elif notcpuflag(avx512)
                    %assign __emulate_avx 1
                %endif
            %endif
            %if __emulate_avx ; a separate load is required
                %if %3
                    vmovaps %6, %7
                %else
                    vmovdqa %6, %7
                %endif
                __instr %6, %6, %8
            %else
                __instr %6, __src1, __src2
            %endif
        %else
            __instr %6, %7, %8
        %endif
    %elif %0 == 7
        %if avx_enabled && __sizeofreg >= 16 && %5
            %xdefine __src1 %6
            %xdefine __src2 %7
            %ifnum regnumof%6
                %ifnum regnumof%7
                    %if regnumof%6 < 8 && regnumof%7 >= 8 && regnumof%7 < 16 && sizeof%7 <= 32
                        %xdefine __src1 %7
                        %xdefine __src2 %6
                    %endif
                %endif
            %endif
            __instr %6, __src1, __src2
        %else
            __instr %6, %7
        %endif
    %else
        __instr %6
    %endif
%endmacro

;%1 == instruction
;%2 == minimal instruction set
;%3 == 1 if float, 0 if int
;%4 == 1 if 4-operand emulation, 0 if 3-operand emulation, 255 otherwise (no emulation)
;%5 == 1 if commutative (i.e. doesn't matter which src arg is which), 0 if not
%macro AVX_INSTR 1-5 fnord, 0, 255, 0
    %macro %1 1-10 fnord, fnord, fnord, fnord, %1, %2, %3, %4, %5
        %ifidn %2, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1
        %elifidn %3, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2
        %elifidn %4, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2, %3
        %elifidn %5, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2, %3, %4
        %else
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2, %3, %4, %5
        %endif
    %endmacro
%endmacro

; Instructions with both VEX/EVEX and legacy encodings
; Non-destructive instructions are written without parameters
AVX_INSTR addpd, sse2, 1, 0, 1
AVX_INSTR addps, sse, 1, 0, 1
AVX_INSTR addsd, sse2, 1, 0, 0
AVX_INSTR addss, sse, 1, 0, 0
AVX_INSTR addsubpd, sse3, 1, 0, 0
AVX_INSTR addsubps, sse3, 1, 0, 0
AVX_INSTR aesdec, aesni, 0, 0, 0
AVX_INSTR aesdeclast, aesni, 0, 0, 0
AVX_INSTR aesenc, aesni, 0, 0, 0
AVX_INSTR aesenclast, aesni, 0, 0, 0
AVX_INSTR aesimc, aesni
AVX_INSTR aeskeygenassist, aesni
AVX_INSTR andnpd, sse2, 1, 0, 0
AVX_INSTR andnps, sse, 1, 0, 0
AVX_INSTR andpd, sse2, 1, 0, 1
AVX_INSTR andps, sse, 1, 0, 1
AVX_INSTR blendpd, sse4, 1, 1, 0
AVX_INSTR blendps, sse4, 1, 1, 0
AVX_INSTR blendvpd, sse4, 1, 1, 0 ; last operand must be xmm0 with legacy encoding
AVX_INSTR blendvps, sse4, 1, 1, 0 ; last operand must be xmm0 with legacy encoding
AVX_INSTR cmpeqpd, sse2, 1, 0, 1
AVX_INSTR cmpeqps, sse, 1, 0, 1
AVX_INSTR cmpeqsd, sse2, 1, 0, 0
AVX_INSTR cmpeqss, sse, 1, 0, 0
AVX_INSTR cmplepd, sse2, 1, 0, 0
AVX_INSTR cmpleps, sse, 1, 0, 0
AVX_INSTR cmplesd, sse2, 1, 0, 0
AVX_INSTR cmpless, sse, 1, 0, 0
AVX_INSTR cmpltpd, sse2, 1, 0, 0
AVX_INSTR cmpltps, sse, 1, 0, 0
AVX_INSTR cmpltsd, sse2, 1, 0, 0
AVX_INSTR cmpltss, sse, 1, 0, 0
AVX_INSTR cmpneqpd, sse2, 1, 0, 1
AVX_INSTR cmpneqps, sse, 1, 0, 1
AVX_INSTR cmpneqsd, sse2, 1, 0, 0
AVX_INSTR cmpneqss, sse, 1, 0, 0
AVX_INSTR cmpnlepd, sse2, 1, 0, 0
AVX_INSTR cmpnleps, sse, 1, 0, 0
AVX_INSTR cmpnlesd, sse2, 1, 0, 0
AVX_INSTR cmpnless, sse, 1, 0, 0
AVX_INSTR cmpnltpd, sse2, 1, 0, 0
AVX_INSTR cmpnltps, sse, 1, 0, 0
AVX_INSTR cmpnltsd, sse2, 1, 0, 0
AVX_INSTR cmpnltss, sse, 1, 0, 0
AVX_INSTR cmpordpd, sse2 1, 0, 1
AVX_INSTR cmpordps, sse 1, 0, 1
AVX_INSTR cmpordsd, sse2 1, 0, 0
AVX_INSTR cmpordss, sse 1, 0, 0
AVX_INSTR cmppd, sse2, 1, 1, 0
AVX_INSTR cmpps, sse, 1, 1, 0
AVX_INSTR cmpsd, sse2, 1, 1, 0
AVX_INSTR cmpss, sse, 1, 1, 0
AVX_INSTR cmpunordpd, sse2, 1, 0, 1
AVX_INSTR cmpunordps, sse, 1, 0, 1
AVX_INSTR cmpunordsd, sse2, 1, 0, 0
AVX_INSTR cmpunordss, sse, 1, 0, 0
AVX_INSTR comisd, sse2, 1
AVX_INSTR comiss, sse, 1
AVX_INSTR cvtdq2pd, sse2, 1
AVX_INSTR cvtdq2ps, sse2, 1
AVX_INSTR cvtpd2dq, sse2, 1
AVX_INSTR cvtpd2ps, sse2, 1
AVX_INSTR cvtps2dq, sse2, 1
AVX_INSTR cvtps2pd, sse2, 1
AVX_INSTR cvtsd2si, sse2, 1
AVX_INSTR cvtsd2ss, sse2, 1, 0, 0
AVX_INSTR cvtsi2sd, sse2, 1, 0, 0
AVX_INSTR cvtsi2ss, sse, 1, 0, 0
AVX_INSTR cvtss2sd, sse2, 1, 0, 0
AVX_INSTR cvtss2si, sse, 1
AVX_INSTR cvttpd2dq, sse2, 1
AVX_INSTR cvttps2dq, sse2, 1
AVX_INSTR cvttsd2si, sse2, 1
AVX_INSTR cvttss2si, sse, 1
AVX_INSTR divpd, sse2, 1, 0, 0
AVX_INSTR divps, sse, 1, 0, 0
AVX_INSTR divsd, sse2, 1, 0, 0
AVX_INSTR divss, sse, 1, 0, 0
AVX_INSTR dppd, sse4, 1, 1, 0
AVX_INSTR dpps, sse4, 1, 1, 0
AVX_INSTR extractps, sse4, 1
AVX_INSTR gf2p8affineinvqb, gfni, 0, 1, 0
AVX_INSTR gf2p8affineqb, gfni, 0, 1, 0
AVX_INSTR gf2p8mulb, gfni, 0, 0, 0
AVX_INSTR haddpd, sse3, 1, 0, 0
AVX_INSTR haddps, sse3, 1, 0, 0
AVX_INSTR hsubpd, sse3, 1, 0, 0
AVX_INSTR hsubps, sse3, 1, 0, 0
AVX_INSTR insertps, sse4, 1, 1, 0
AVX_INSTR lddqu, sse3
AVX_INSTR ldmxcsr, sse, 1
AVX_INSTR maskmovdqu, sse2
AVX_INSTR maxpd, sse2, 1, 0, 1
AVX_INSTR maxps, sse, 1, 0, 1
AVX_INSTR maxsd, sse2, 1, 0, 0
AVX_INSTR maxss, sse, 1, 0, 0
AVX_INSTR minpd, sse2, 1, 0, 1
AVX_INSTR minps, sse, 1, 0, 1
AVX_INSTR minsd, sse2, 1, 0, 0
AVX_INSTR minss, sse, 1, 0, 0
AVX_INSTR movapd, sse2, 1
AVX_INSTR movaps, sse, 1
AVX_INSTR movd, mmx
AVX_INSTR movddup, sse3, 1
AVX_INSTR movdqa, sse2
AVX_INSTR movdqu, sse2
AVX_INSTR movhlps, sse, 1, 0, 0
AVX_INSTR movhpd, sse2, 1, 0, 0
AVX_INSTR movhps, sse, 1, 0, 0
AVX_INSTR movlhps, sse, 1, 0, 0
AVX_INSTR movlpd, sse2, 1, 0, 0
AVX_INSTR movlps, sse, 1, 0, 0
AVX_INSTR movmskpd, sse2, 1
AVX_INSTR movmskps, sse, 1
AVX_INSTR movntdq, sse2
AVX_INSTR movntdqa, sse4
AVX_INSTR movntpd, sse2, 1
AVX_INSTR movntps, sse, 1
AVX_INSTR movq, mmx
AVX_INSTR movsd, sse2, 1, 0, 0
AVX_INSTR movshdup, sse3, 1
AVX_INSTR movsldup, sse3, 1
AVX_INSTR movss, sse, 1, 0, 0
AVX_INSTR movupd, sse2, 1
AVX_INSTR movups, sse, 1
AVX_INSTR mpsadbw, sse4, 0, 1, 0
AVX_INSTR mulpd, sse2, 1, 0, 1
AVX_INSTR mulps, sse, 1, 0, 1
AVX_INSTR mulsd, sse2, 1, 0, 0
AVX_INSTR mulss, sse, 1, 0, 0
AVX_INSTR orpd, sse2, 1, 0, 1
AVX_INSTR orps, sse, 1, 0, 1
AVX_INSTR pabsb, ssse3
AVX_INSTR pabsd, ssse3
AVX_INSTR pabsw, ssse3
AVX_INSTR packssdw, mmx, 0, 0, 0
AVX_INSTR packsswb, mmx, 0, 0, 0
AVX_INSTR packusdw, sse4, 0, 0, 0
AVX_INSTR packuswb, mmx, 0, 0, 0
AVX_INSTR paddb, mmx, 0, 0, 1
AVX_INSTR paddd, mmx, 0, 0, 1
AVX_INSTR paddq, sse2, 0, 0, 1
AVX_INSTR paddsb, mmx, 0, 0, 1
AVX_INSTR paddsw, mmx, 0, 0, 1
AVX_INSTR paddusb, mmx, 0, 0, 1
AVX_INSTR paddusw, mmx, 0, 0, 1
AVX_INSTR paddw, mmx, 0, 0, 1
AVX_INSTR palignr, ssse3, 0, 1, 0
AVX_INSTR pand, mmx, 0, 0, 1
AVX_INSTR pandn, mmx, 0, 0, 0
AVX_INSTR pavgb, mmx2, 0, 0, 1
AVX_INSTR pavgw, mmx2, 0, 0, 1
AVX_INSTR pblendvb, sse4, 0, 1, 0 ; last operand must be xmm0 with legacy encoding
AVX_INSTR pblendw, sse4, 0, 1, 0
AVX_INSTR pclmulhqhqdq, clmul, 0, 0, 0
AVX_INSTR pclmulhqlqdq, clmul, 0, 0, 0
AVX_INSTR pclmullqhqdq, clmul, 0, 0, 0
AVX_INSTR pclmullqlqdq, clmul, 0, 0, 0
AVX_INSTR pclmulqdq, clmul, 0, 1, 0
AVX_INSTR pcmpeqb, mmx, 0, 0, 1
AVX_INSTR pcmpeqd, mmx, 0, 0, 1
AVX_INSTR pcmpeqq, sse4, 0, 0, 1
AVX_INSTR pcmpeqw, mmx, 0, 0, 1
AVX_INSTR pcmpestri, sse42
AVX_INSTR pcmpestrm, sse42
AVX_INSTR pcmpgtb, mmx, 0, 0, 0
AVX_INSTR pcmpgtd, mmx, 0, 0, 0
AVX_INSTR pcmpgtq, sse42, 0, 0, 0
AVX_INSTR pcmpgtw, mmx, 0, 0, 0
AVX_INSTR pcmpistri, sse42
AVX_INSTR pcmpistrm, sse42
AVX_INSTR pextrb, sse4
AVX_INSTR pextrd, sse4
AVX_INSTR pextrq, sse4
AVX_INSTR pextrw, mmx2
AVX_INSTR phaddd, ssse3, 0, 0, 0
AVX_INSTR phaddsw, ssse3, 0, 0, 0
AVX_INSTR phaddw, ssse3, 0, 0, 0
AVX_INSTR phminposuw, sse4
AVX_INSTR phsubd, ssse3, 0, 0, 0
AVX_INSTR phsubsw, ssse3, 0, 0, 0
AVX_INSTR phsubw, ssse3, 0, 0, 0
AVX_INSTR pinsrb, sse4, 0, 1, 0
AVX_INSTR pinsrd, sse4, 0, 1, 0
AVX_INSTR pinsrq, sse4, 0, 1, 0
AVX_INSTR pinsrw, mmx2, 0, 1, 0
AVX_INSTR pmaddubsw, ssse3, 0, 0, 0
AVX_INSTR pmaddwd, mmx, 0, 0, 1
AVX_INSTR pmaxsb, sse4, 0, 0, 1
AVX_INSTR pmaxsd, sse4, 0, 0, 1
AVX_INSTR pmaxsw, mmx2, 0, 0, 1
AVX_INSTR pmaxub, mmx2, 0, 0, 1
AVX_INSTR pmaxud, sse4, 0, 0, 1
AVX_INSTR pmaxuw, sse4, 0, 0, 1
AVX_INSTR pminsb, sse4, 0, 0, 1
AVX_INSTR pminsd, sse4, 0, 0, 1
AVX_INSTR pminsw, mmx2, 0, 0, 1
AVX_INSTR pminub, mmx2, 0, 0, 1
AVX_INSTR pminud, sse4, 0, 0, 1
AVX_INSTR pminuw, sse4, 0, 0, 1
AVX_INSTR pmovmskb, mmx2
AVX_INSTR pmovsxbd, sse4
AVX_INSTR pmovsxbq, sse4
AVX_INSTR pmovsxbw, sse4
AVX_INSTR pmovsxdq, sse4
AVX_INSTR pmovsxwd, sse4
AVX_INSTR pmovsxwq, sse4
AVX_INSTR pmovzxbd, sse4
AVX_INSTR pmovzxbq, sse4
AVX_INSTR pmovzxbw, sse4
AVX_INSTR pmovzxdq, sse4
AVX_INSTR pmovzxwd, sse4
AVX_INSTR pmovzxwq, sse4
AVX_INSTR pmuldq, sse4, 0, 0, 1
AVX_INSTR pmulhrsw, ssse3, 0, 0, 1
AVX_INSTR pmulhuw, mmx2, 0, 0, 1
AVX_INSTR pmulhw, mmx, 0, 0, 1
AVX_INSTR pmulld, sse4, 0, 0, 1
AVX_INSTR pmullw, mmx, 0, 0, 1
AVX_INSTR pmuludq, sse2, 0, 0, 1
AVX_INSTR por, mmx, 0, 0, 1
AVX_INSTR psadbw, mmx2, 0, 0, 1
AVX_INSTR pshufb, ssse3, 0, 0, 0
AVX_INSTR pshufd, sse2
AVX_INSTR pshufhw, sse2
AVX_INSTR pshuflw, sse2
AVX_INSTR psignb, ssse3, 0, 0, 0
AVX_INSTR psignd, ssse3, 0, 0, 0
AVX_INSTR psignw, ssse3, 0, 0, 0
AVX_INSTR pslld, mmx, 0, 0, 0
AVX_INSTR pslldq, sse2, 0, 0, 0
AVX_INSTR psllq, mmx, 0, 0, 0
AVX_INSTR psllw, mmx, 0, 0, 0
AVX_INSTR psrad, mmx, 0, 0, 0
AVX_INSTR psraw, mmx, 0, 0, 0
AVX_INSTR psrld, mmx, 0, 0, 0
AVX_INSTR psrldq, sse2, 0, 0, 0
AVX_INSTR psrlq, mmx, 0, 0, 0
AVX_INSTR psrlw, mmx, 0, 0, 0
AVX_INSTR psubb, mmx, 0, 0, 0
AVX_INSTR psubd, mmx, 0, 0, 0
AVX_INSTR psubq, sse2, 0, 0, 0
AVX_INSTR psubsb, mmx, 0, 0, 0
AVX_INSTR psubsw, mmx, 0, 0, 0
AVX_INSTR psubusb, mmx, 0, 0, 0
AVX_INSTR psubusw, mmx, 0, 0, 0
AVX_INSTR psubw, mmx, 0, 0, 0
AVX_INSTR ptest, sse4
AVX_INSTR punpckhbw, mmx, 0, 0, 0
AVX_INSTR punpckhdq, mmx, 0, 0, 0
AVX_INSTR punpckhqdq, sse2, 0, 0, 0
AVX_INSTR punpckhwd, mmx, 0, 0, 0
AVX_INSTR punpcklbw, mmx, 0, 0, 0
AVX_INSTR punpckldq, mmx, 0, 0, 0
AVX_INSTR punpcklqdq, sse2, 0, 0, 0
AVX_INSTR punpcklwd, mmx, 0, 0, 0
AVX_INSTR pxor, mmx, 0, 0, 1
AVX_INSTR rcpps, sse, 1
AVX_INSTR rcpss, sse, 1, 0, 0
AVX_INSTR roundpd, sse4, 1
AVX_INSTR roundps, sse4, 1
AVX_INSTR roundsd, sse4, 1, 1, 0
AVX_INSTR roundss, sse4, 1, 1, 0
AVX_INSTR rsqrtps, sse, 1
AVX_INSTR rsqrtss, sse, 1, 0, 0
AVX_INSTR shufpd, sse2, 1, 1, 0
AVX_INSTR shufps, sse, 1, 1, 0
AVX_INSTR sqrtpd, sse2, 1
AVX_INSTR sqrtps, sse, 1
AVX_INSTR sqrtsd, sse2, 1, 0, 0
AVX_INSTR sqrtss, sse, 1, 0, 0
AVX_INSTR stmxcsr, sse, 1
AVX_INSTR subpd, sse2, 1, 0, 0
AVX_INSTR subps, sse, 1, 0, 0
AVX_INSTR subsd, sse2, 1, 0, 0
AVX_INSTR subss, sse, 1, 0, 0
AVX_INSTR ucomisd, sse2, 1
AVX_INSTR ucomiss, sse, 1
AVX_INSTR unpckhpd, sse2, 1, 0, 0
AVX_INSTR unpckhps, sse, 1, 0, 0
AVX_INSTR unpcklpd, sse2, 1, 0, 0
AVX_INSTR unpcklps, sse, 1, 0, 0
AVX_INSTR xorpd, sse2, 1, 0, 1
AVX_INSTR xorps, sse, 1, 0, 1

; 3DNow instructions, for sharing code between AVX, SSE and 3DN
AVX_INSTR pfadd, 3dnow, 1, 0, 1
AVX_INSTR pfmul, 3dnow, 1, 0, 1
AVX_INSTR pfsub, 3dnow, 1, 0, 0

;%1 == instruction
;%2 == minimal instruction set
%macro GPR_INSTR 2
    %macro %1 2-5 fnord, %1, %2
        %ifdef cpuname
            %if notcpuflag(%5)
                %error use of ``%4'' %5 instruction in cpuname function: current_function
            %endif
        %endif
        %ifidn %3, fnord
            %4 %1, %2
        %else
            %4 %1, %2, %3
        %endif
    %endmacro
%endmacro

GPR_INSTR andn, bmi1
GPR_INSTR bextr, bmi1
GPR_INSTR blsi, bmi1
GPR_INSTR blsmsk, bmi1
GPR_INSTR blsr, bmi1
GPR_INSTR bzhi, bmi2
GPR_INSTR crc32, sse42
GPR_INSTR mulx, bmi2
GPR_INSTR pdep, bmi2
GPR_INSTR pext, bmi2
GPR_INSTR popcnt, sse42
GPR_INSTR rorx, bmi2
GPR_INSTR sarx, bmi2
GPR_INSTR shlx, bmi2
GPR_INSTR shrx, bmi2

; base-4 constants for shuffles
%assign i 0
%rep 256
    %assign j ((i>>6)&3)*1000 + ((i>>4)&3)*100 + ((i>>2)&3)*10 + (i&3)
    %if j < 10
        CAT_XDEFINE q000, j, i
    %elif j < 100
        CAT_XDEFINE q00, j, i
    %elif j < 1000
        CAT_XDEFINE q0, j, i
    %else
        CAT_XDEFINE q, j, i
    %endif
    %assign i i+1
%endrep
%undef i
%undef j

%macro FMA_INSTR 3
    %macro %1 4-7 %1, %2, %3
        %if cpuflag(xop)
            v%5 %1, %2, %3, %4
        %elifnidn %1, %4
            %6 %1, %2, %3
            %7 %1, %4
        %else
            %error non-xop emulation of ``%5 %1, %2, %3, %4'' is not supported
        %endif
    %endmacro
%endmacro

FMA_INSTR pmacsdd,  pmulld,  paddd ; sse4 emulation
FMA_INSTR pmacsdql, pmuldq,  paddq ; sse4 emulation
FMA_INSTR pmacsww,  pmullw,  paddw
FMA_INSTR pmadcswd, pmaddwd, paddd

; Macros for consolidating FMA3 and FMA4 using 4-operand (dst, src1, src2, src3) syntax.
; FMA3 is only possible if dst is the same as one of the src registers.
; Either src2 or src3 can be a memory operand.
%macro FMA4_INSTR 2-*
    %push fma4_instr
    %xdefine %$prefix %1
    %rep %0 - 1
        %macro %$prefix%2 4-6 %$prefix, %2
            %if notcpuflag(fma3) && notcpuflag(fma4)
                %error use of ``%5%6'' fma instruction in cpuname function: current_function
            %elif cpuflag(fma4)
                v%5%6 %1, %2, %3, %4
            %elifidn %1, %2
                ; If %3 or %4 is a memory operand it needs to be encoded as the last operand.
                %ifnum sizeof%3
                    v%{5}213%6 %2, %3, %4
                %else
                    v%{5}132%6 %2, %4, %3
                %endif
            %elifidn %1, %3
                v%{5}213%6 %3, %2, %4
            %elifidn %1, %4
                v%{5}231%6 %4, %2, %3
            %else
                %error fma3 emulation of ``%5%6 %1, %2, %3, %4'' is not supported
            %endif
        %endmacro
        %rotate 1
    %endrep
    %pop
%endmacro

FMA4_INSTR fmadd,    pd, ps, sd, ss
FMA4_INSTR fmaddsub, pd, ps
FMA4_INSTR fmsub,    pd, ps, sd, ss
FMA4_INSTR fmsubadd, pd, ps
FMA4_INSTR fnmadd,   pd, ps, sd, ss
FMA4_INSTR fnmsub,   pd, ps, sd, ss

; Macros for converting VEX instructions to equivalent EVEX ones.
%macro EVEX_INSTR 2-3 0 ; vex, evex, prefer_evex
    %macro %1 2-7 fnord, fnord, %1, %2, %3
        %ifidn %3, fnord
            %define %%args %1, %2
        %elifidn %4, fnord
            %define %%args %1, %2, %3
        %else
            %define %%args %1, %2, %3, %4
        %endif
        %assign %%evex_required cpuflag(avx512) & %7
        %ifnum regnumof%1
            %if regnumof%1 >= 16 || sizeof%1 > 32
                %assign %%evex_required 1
            %endif
        %endif
        %ifnum regnumof%2
            %if regnumof%2 >= 16 || sizeof%2 > 32
                %assign %%evex_required 1
            %endif
        %endif
        %ifnum regnumof%3
            %if regnumof%3 >= 16 || sizeof%3 > 32
                %assign %%evex_required 1
            %endif
        %endif
        %if %%evex_required
            %6 %%args
        %else
            %5 %%args ; Prefer VEX over EVEX due to shorter instruction length
        %endif
    %endmacro
%endmacro

EVEX_INSTR vbroadcastf128, vbroadcastf32x4
EVEX_INSTR vbroadcasti128, vbroadcasti32x4
EVEX_INSTR vextractf128,   vextractf32x4
EVEX_INSTR vextracti128,   vextracti32x4
EVEX_INSTR vinsertf128,    vinsertf32x4
EVEX_INSTR vinserti128,    vinserti32x4
EVEX_INSTR vmovdqa,        vmovdqa32
EVEX_INSTR vmovdqu,        vmovdqu32
EVEX_INSTR vpand,          vpandd
EVEX_INSTR vpandn,         vpandnd
EVEX_INSTR vpor,           vpord
EVEX_INSTR vpxor,          vpxord
EVEX_INSTR vrcpps,         vrcp14ps,   1 ; EVEX versions have higher precision
EVEX_INSTR vrcpss,         vrcp14ss,   1
EVEX_INSTR vrsqrtps,       vrsqrt14ps, 1
EVEX_INSTR vrsqrtss,       vrsqrt14ss, 1
```

## Little CMS 2 — 2.19.1

License: MIT

Upstream: https://github.com/mm2/Little-CMS

### licenses/pillow-lcms2/LICENSE

```text
MIT License

Copyright (c) 2023 Marti Maria Saguer

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## libXau — 1.0.9-3.el8

License: X11/MIT-style

Upstream: https://www.x.org/releases/individual/lib/libXau-1.0.9.tar.bz2

### licenses/pillow-libXau/COPYING

```text
Copyright 1988, 1993, 1994, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.
```

## libaom (inside libavif) — 3.14.1

License: BSD-2-Clause + patent grant

Upstream: https://aomedia.googlesource.com/aom/

### licenses/pillow-libaom/LICENSE

```text
Copyright (c) 2016, Alliance for Open Media. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libaom/PATENTS

```text
Alliance for Open Media Patent License 1.0

1. License Terms.

1.1. Patent License. Subject to the terms and conditions of this License, each
     Licensor, on behalf of itself and successors in interest and assigns,
     grants Licensee a non-sublicensable, perpetual, worldwide, non-exclusive,
     no-charge, royalty-free, irrevocable (except as expressly stated in this
     License) patent license to its Necessary Claims to make, use, sell, offer
     for sale, import or distribute any Implementation.

1.2. Conditions.

1.2.1. Availability. As a condition to the grant of rights to Licensee to make,
       sell, offer for sale, import or distribute an Implementation under
       Section 1.1, Licensee must make its Necessary Claims available under
       this License, and must reproduce this License with any Implementation
       as follows:

       a. For distribution in source code, by including this License in the
          root directory of the source code with its Implementation.

       b. For distribution in any other form (including binary, object form,
          and/or hardware description code (e.g., HDL, RTL, Gate Level Netlist,
          GDSII, etc.)), by including this License in the documentation, legal
          notices, and/or other written materials provided with the
          Implementation.

1.2.2. Additional Conditions. This license is directly from Licensor to
       Licensee.  Licensee acknowledges as a condition of benefiting from it
       that no rights from Licensor are received from suppliers, distributors,
       or otherwise in connection with this License.

1.3. Defensive Termination. If any Licensee, its Affiliates, or its agents
     initiates patent litigation or files, maintains, or voluntarily
     participates in a lawsuit against another entity or any person asserting
     that any Implementation infringes Necessary Claims, any patent licenses
     granted under this License directly to the Licensee are immediately
     terminated as of the date of the initiation of action unless 1) that suit
     was in response to a corresponding suit regarding an Implementation first
     brought against an initiating entity, or 2) that suit was brought to
     enforce the terms of this License (including intervention in a third-party
     action by a Licensee).

1.4. Disclaimers. The Reference Implementation and Specification are provided
     "AS IS" and without warranty. The entire risk as to implementing or
     otherwise using the Reference Implementation or Specification is assumed
     by the implementer and user. Licensor expressly disclaims any warranties
     (express, implied, or otherwise), including implied warranties of
     merchantability, non-infringement, fitness for a particular purpose, or
     title, related to the material. IN NO EVENT WILL LICENSOR BE LIABLE TO
     ANY OTHER PARTY FOR LOST PROFITS OR ANY FORM OF INDIRECT, SPECIAL,
     INCIDENTAL, OR CONSEQUENTIAL DAMAGES OF ANY CHARACTER FROM ANY CAUSES OF
     ACTION OF ANY KIND WITH RESPECT TO THIS LICENSE, WHETHER BASED ON BREACH
     OF CONTRACT, TORT (INCLUDING NEGLIGENCE), OR OTHERWISE, AND WHETHER OR
     NOT THE OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

2. Definitions.

2.1. Affiliate.  "Affiliate" means an entity that directly or indirectly
     Controls, is Controlled by, or is under common Control of that party.

2.2. Control. "Control" means direct or indirect control of more than 50% of
     the voting power to elect directors of that corporation, or for any other
     entity, the power to direct management of such entity.

2.3. Decoder.  "Decoder" means any decoder that conforms fully with all
     non-optional portions of the Specification.

2.4. Encoder.  "Encoder" means any encoder that produces a bitstream that can
     be decoded by a Decoder only to the extent it produces such a bitstream.

2.5. Final Deliverable.  "Final Deliverable" means the final version of a
     deliverable approved by the Alliance for Open Media as a Final
     Deliverable.

2.6. Implementation.  "Implementation" means any implementation, including the
     Reference Implementation, that is an Encoder and/or a Decoder. An
     Implementation also includes components of an Implementation only to the
     extent they are used as part of an Implementation.

2.7. License. "License" means this license.

2.8. Licensee. "Licensee" means any person or entity who exercises patent
     rights granted under this License.

2.9. Licensor.  "Licensor" means (i) any Licensee that makes, sells, offers
     for sale, imports or distributes any Implementation, or (ii) a person
     or entity that has a licensing obligation to the Implementation as a
     result of its membership and/or participation in the Alliance for Open
     Media working group that developed the Specification.

2.10. Necessary Claims.  "Necessary Claims" means all claims of patents or
      patent applications, (a) that currently or at any time in the future,
      are owned or controlled by the Licensor, and (b) (i) would be an
      Essential Claim as defined by the W3C Policy as of February 5, 2004
      (https://www.w3.org/Consortium/Patent-Policy-20040205/#def-essential)
      as if the Specification was a W3C Recommendation; or (ii) are infringed
      by the Reference Implementation.

2.11. Reference Implementation. "Reference Implementation" means an Encoder
      and/or Decoder released by the Alliance for Open Media as a Final
      Deliverable.

2.12. Specification. "Specification" means the specification designated by
      the Alliance for Open Media as a Final Deliverable for which this
      License was issued.
```

### licenses/pillow-libaom/AUTHORS

```text
# This file is automatically generated from the git commit history
# by tools/gen_authors.sh.

Aamir Anis <aanis@google.com>
Aaron Watry <awatry@gmail.com>
Aasaipriya Chandran <aasaipriya.c@ittiam.com>
Abo Talib Mahfoodh <ab.mahfoodh@gmail.com>
Adrian Grange <agrange@google.com>
Ahmad Sharif <asharif@google.com>
Akshata Jadhav <akshata.jadhav@ittiam.com>
Alexander Bokov <alexanderbokov@google.com>
Alexander Voronov <avoronov@graphics.cs.msu.ru>
Aℓex Converse <aconverse@google.com>
Alex Davicenko <alex.davicenko@arm.com>
Alex Faxa <alexanderfaxa@google.com>
Alexis Ballier <aballier@gentoo.org>
Alex Peterson <petersonab@google.com>
Alok Ahuja <waveletcoeff@gmail.com>
Alpha Lam <hclam@google.com>
A.Mahfoodh <ab.mahfoodh@gmail.com>
Ami Fischman <fischman@chromium.org>
Andoni Morales Alastruey <ylatuya@gmail.com>
Andres Mejia <mcitadel@gmail.com>
Andrew Russell <anrussell@google.com>
Andrey Norkin <anorkin@netflix.com>
Angie Chiang <angiebird@google.com>
Aniket Dhok <aniket.dhok@ittiam.com>
Aniket Wanare <Aniket.wanare@ittiam.com>
Ankur Saxena <ankurs@nvidia.com>
Anupam Pandey <anupam.pandey@ittiam.com>
Anusuya <anusuya.k@ittiam.com>
Apurve Kumar Pandey <apurve.pandey@ittiam.com>
Aras Pranckevicius <aras@nesnausk.org>
Arild Fuldseth <arilfuld@cisco.com>
Aron Rosenberg <arosenberg@logitech.com>
Arpad Panyik <Arpad.Panyik@arm.com>
Arun Singh Negi <arun.negi@ittiam.com>
Athulya Raj Raji Mohini <AthulyaRaj.RajiMohini@arm.com>
Attila Nagy <attilanagy@google.com>
Balaji Anandapadmanaban <balaji.anandapadmanaban@arm.com>
Bernhard M. Wiedemann <bwiedemann@suse.de>
Bhaskarabhatla V S K S Yaswanth Sastry <yaswanth.sastry@ittiam.com>
bmarques1995 <testebash@outlook.com>
Bohan Li <bohanli@google.com>
Brennan Shacklett <bshacklett@mozilla.com>
Brion Vibber <bvibber@wikimedia.org>
Bruno Berthier <bruno.berthier@allegrodvt.com>
Casey Smalley <casey.smalley@arm.com>
Changjun Yang <changjun.yang@intel.com>
Charles 'Buck' Krasic <ckrasic@google.com>
Cheng Chen <chengchen@google.com>
Cherma Rajan A <cherma.rajan@ittiam.com>
Chethan Kumar R E <chethan.kumar@ittiam.com>
Chi Yo Tsai <chiyotsai@google.com>
Chm <chm@rock-chips.com>
Christian Duvivier <cduvivier@google.com>
Christopher Degawa <christopher.degawa@intel.com>
Cyril Concolato <cconcolato@netflix.com>
Dake He <dkhe@google.com>
Damon Shen <yjshen@google.com>
Dandan Ding <vickyddding@gmail.com>
Daniel Cheng <dcheng@chromium.org>
Daniele Castagna <dcastagna@chromium.org>
Daniel Kang <ddkang@google.com>
Daniel Max Valenzuela <daniel.vt@samsung.com>
Danil Chapovalov <danilchap@google.com>
Darryl Pogue <darryl@dpogue.ca>
David Major <dmajor@mozilla.com>
David Michael Barr <b@rr-dav.id.au>
David Turner <david.turner@argondesign.com>
Deb Mukherjee <debargha@google.com>
Deepa K G <deepa.kg@ittiam.com>
Denis Nikitin <denik@google.com>
Di Chen <chendixi@google.com>
Diksha Singh <diksha.singh@ittiam.com>
Dim Temp <dimtemp0@gmail.com>
Dmitry Kovalev <dkovalev@google.com>
Dominic Symes <dominic.symes@arm.com>
Dragan Mrdjan <dmrdjan@mips.com>
Ed Baker <edward.baker@intel.com>
Edward Hervey <edward@centricular.com>
Ehsan Akhgari <ehsan.akhgari@gmail.com>
Elliott Karpilovsky <elliottk@google.com>
Emil Keyder <emilkeyder@google.com>
Erik Niemeyer <erik.a.niemeyer@intel.com>
Erik Språng <sprang@google.com>
Fabio Pedretti <fabio.ped@libero.it>
Fangwen Fu <fangwen.fu@intel.com>
Fergus Simpson <afergs@google.com>
Frank Bossen <fbossen@gmail.com>
Frank Galligan <fgalligan@google.com>
Frederic Barbier <frederic.barbier@allegrodvt.com>
Fredrik Söderquist <fs@opera.com>
Fritz Koenig <frkoenig@google.com>
Fyodor Kyslov <kyslov@google.com>
Gaute Strokkenes <gaute.strokkenes@broadcom.com>
George Steed <george.steed@arm.com>
Gerda Zsejke More <gerdazsejke.more@arm.com>
Geza Lore <gezalore@gmail.com>
Ghislain MARY <ghislainmary2@gmail.com>
Giuseppe Scrivano <gscrivano@gnu.org>
Gordana Cmiljanovic <gordana.cmiljanovic@imgtec.com>
Grant Hsu <grant.hsu@cidana.com>
Guillaume Martres <smarter@ubuntu.com>
Guillermo Ballester Valor <gbvalor@gmail.com>
Hamsalekha S <hamsalekha.s@ittiam.com>
Hangyu Kuang <hkuang@google.com>
Hanno Böck <hanno@hboeck.de>
Hari Limaye <hari.limaye@arm.com>
Harish Mahendrakar <harish.mahendrakar@ittiam.com>
Henrik Lundin <hlundin@google.com>
Hien Ho <hienho@google.com>
Hirokazu Honda <hiroh@google.com>
Hui Su <huisu@google.com>
Ilie Halip <ilie.halip@gmail.com>
Ilya Brailovskiy <brailovs@lab126.com>
Imdad Sardharwalla <imdad.sardharwalla@argondesign.com>
Iole Moccagatta <iole.moccagatta@gmail.com>
Ivan Krasin <krasin@chromium.org>
Ivan Maltz <ivanmaltz@google.com>
Ivan Rosales <rosalesi@google.com>
Jacek Caban <cjacek@gmail.com>
Jack Haughton <jack.haughton@argondesign.com>
Jacky Chen <jackychen@google.com>
James Berry <jamesberry@google.com>
James Yu <james.yu@linaro.org>
James Zern <jzern@google.com>
Jan Gerber <j@mailb.org>
Jan Kratochvil <jan.kratochvil@redhat.com>
Janne Salonen <jsalonen@google.com>
Jayasanker J <jayasanker.j@ittiam.com>
Jayashri Murugan <jayashri.murugan@ittiam.com>
Jean-Marc Valin <jmvalin@jmvalin.ca>
Jean-Yves Avenard <jyavenard@mozilla.com>
Jeff Faust <jfaust@google.com>
Jeff Muizelaar <jmuizelaar@mozilla.com>
Jeff Petkau <jpet@chromium.org>
Jeremy Dorfman <jdorfman@google.com>
Jerome Jiang <jianj@google.com>
jerry <jerytsai@andestech.com>
Jerry Tsai <jerytsai@andestech.com>
Jia Jia <jia.jia@linaro.org>
Jian Zhou <zhoujian@fb.com>
Jim Bankoski <jimbankoski@google.com>
Jingning Han <jingning@google.com>
Joe Young <joeyoung@google.com>
Joey Parrish <joeyparrish@google.com>
Johann Koenig <johannkoenig@google.com>
John Koleszar <jkoleszar@google.com>
Johnny Klonaris <google@jawknee.com>
John Stark <jhnstrk@gmail.com>
Jonathan Matthews <jonathan.matthews@argondesign.com>
Jonathan Wright <jonathan.wright@arm.com>
Jordan Brown <rop@google.com>
Joshua Bleecher Snyder <josh@treelinelabs.com>
Joshua Litt <joshualitt@google.com>
Josh Verdejo <joverdejo@google.com>
Julia Robson <juliamrobson@gmail.com>
Julio Barba <juliobbv@gmail.com>
Justin Clift <justin@salasaga.org>
Justin Lebar <justin.lebar@gmail.com>
Kalamatee <kalamatee@gmail.com>
Katsuhisa Yuasa <berupon@gmail.com>
Kavi Ramamurthy <kavii@google.com>
KO Myung-Hun <komh@chollian.net>
Konstantinos Margaritis <konma@vectorcamp.gr>
Krishna Malladi <kmalladi@google.com>
Kwanghoon Son <kwangson@yahoo.com>
Kyle Siefring <siekyleb@amazon.com>
Kyle Swanson <kswanson@netflix.com>
Larisa Markeeva <lmarkeeva@google.com>
Lauren Partin <lpartin@google.com>
Lawrence Velázquez <larryv@macports.org>
leolzhao <leolzhao@tencent.com>
Leon Kollar <Leon.Kollar@arm.com>
L. E. Segovia <amy@amyspark.me>
Lester Lu <kslu@google.com>
liang zhao <leolzhao@tencent.com>
Linfeng Zhang <linfengz@google.com>
Link.Meng <monthev@gmail.com>
Lin Zheng <linzhen@google.com>
Li Zhang <li.zhang2@arm.com>
Logan Goldberg <logangw@google.com>
Lokeshwar Reddy B <lokeshwar.reddy@ittiam.com>
Lou Quillio <louquillio@google.com>
Luca Barbato <lu_zero@gentoo.org>
Luca Versari <veluca@google.com>
Luc Trudeau <luc@trud.ca>
Madhu Peringassery Krishnan <mpkrishnan@tencent.com>
Mahesh Madhav <mahesh@amperecomputing.com>
Makoto Kato <makoto.kt@gmail.com>
Mans Rullgard <mans@mansr.com>
Marco Paniconi <marpan@google.com>
Mark Horvath <mark.horvath@arm.com>
Mark Mentovai <mark@chromium.org>
Mark Wachsler <wachsler@google.com>
Martin Ettl <ettl.martin78@googlemail.com>
Martin Storsjo <martin@martin.st>
Maryla <maryla@google.com>
Matthew Heaney <matthewjheaney@chromium.org>
Matthieu Vaudano <matthieu.vaudano@allegrodvt.com>
Mattias Hansson <mattias.hansson@arm.com>
Maxym Dmytrychenko <maxim.d33@gmail.com>
Michael Bebenita <mbebenita@gmail.com>
Michael Horowitz <mhoro@webrtc.org>
Michael Kohler <michaelkohler@live.com>
Michelle Findlay-Olynyk <mfo@google.com>
Mike Frysinger <vapier@chromium.org>
Mike Hommey <mhommey@mozilla.com>
Mikhal Shemer <mikhal@google.com>
Minghai Shang <minghai@google.com>
Mingliang Chen <mlchen@google.com>
Mirko Bonadei <mbonadei@google.com>
Monty Montgomery <cmontgomery@mozilla.com>
Morton Jonuschat <yabawock@gmail.com>
Mudassir Galaganath <mudassir.galaganath@ittiam.com>
Mufaddal Chakera <mufaddal.chakera@ittiam.com>
Narayan Kalaburgi <narayan.kalaburgi@ittiam.com>
Nathan E. Egge <negge@mozilla.com>
Neeraj Gadgil <neeraj.gadgil@ittiam.com>
Neha Mary Thomas <neha.marythomas@ittiam.com>
Neil Birkbeck <birkbeck@google.com>
Nico Weber <thakis@chromium.org>
Nithya V S <nithya.vs@ittiam.com>
Ola Hugosson <ola.hugosson@arm.com>
Oleg Nalivayko <o13g86@gmail.com>
Onur Guleryuz <oguleryuz@google.com>
Parag Salasakar <img.mips1@gmail.com>
Pascal Massimino <pascal.massimino@gmail.com>
Patrik Westin <patrik.westin@gmail.com>
Paul Wilkins <paulwilkins@google.com>
Pavel Frolov <pavel.frolov@vicuesoft.com>
Pavol Rusnak <stick@gk2.sk>
Paweł Hajdan <phajdan@google.com>
Peng Bin <binpengsmail@gmail.com>
Pengchong Jin <pengchong@google.com>
Peter Boström <pbos@google.com>
Peter de Rivaz <peter.derivaz@gmail.com>
Peter Kasting <pkasting@chromium.org>
Philip Jägenstedt <philipj@opera.com>
Philippe Antoine <p.antoine@catenacyber.fr>
Philipp Hancke <phancke@meta.com>
Pradeep Kumar <pradeep.kumar@intel.corp-partner.google.com>
Priit Laes <plaes@plaes.org>
Qiu Jianlin <jianlin.qiu@intel.com>
Rachel Barker <rachelbarker@google.com>
Rafael Ávila de Espíndola <rafael.espindola@gmail.com>
Rafaël Carré <funman@videolan.org>
Ralph Giles <giles@xiph.org>
Ram Mohan M <ram.mohan@ittiam.com>
Ranjit Kumar Tulabandu <ranjit.tulabandu@ittiam.com>
Ravi Chaudhary <ravi.chaudhary@ittiam.com>
Remya Prakasan <remya.prakasan@ittiam.com>
Remy Foray <remy.foray@allegrodvt.com>
Rob Bradford <rob@linux.intel.com>
Robert-André Mauchin <zebob.m@gmail.com>
Robert Chin <robertchin@google.com>
Roger Zhou <youzhou@microsoft.com>
Rohan Baid <rohan.baid@ittiam.com>
Rohit Athavale <rathaval@xilinx.com>
Ronald S. Bultje <rsbultje@gmail.com>
Rostislav Pehlivanov <rpehlivanov@mozilla.com>
Ruiling Song <ruiling.song@intel.com>
Rui Ueyama <ruiu@google.com>
Ruoyu Zhong <zhongruoyu@outlook.com>
Rupert Swarbrick <rupert.swarbrick@argondesign.com>
Ryan Lei <ryanlei@fb.com>
Ryan Overbeck <rover@google.com>
Sachin Kumar Garg <sachin.kumargarg@ittiam.com>
Sai Deng <sdeng@google.com>
Salome Thirot <salome.thirot@arm.com>
Sami Boukortt <sboukortt@google.com>
Sami Pietilä <samipietila@google.com>
Samuel Thibault <samuel.thibault@ens-lyon.org>
Samuthirika S <samuthirika.s@ittiam.com>
Sarah Parker <sarahparker@google.com>
Sasi Inguva <isasi@google.com>
Satheesh Kumar <satheesh.kumar@ittiam.com>
Satish Kumar Suman <satish.suman@ittiam.com>
Scott Graham <scottmg@chromium.org>
Scott LaVarnway <slavarnway@google.com>
Sean DuBois <sean@siobud.com>
Sean McGovern <gseanmcg@gmail.com>
Sean Purser-Haskell <seanhaskell@google.com>
Sebastien Alaiwan <sebastien.alaiwan@allegrodvt.com>
Sergey Kolomenkin <kolomenkin@gmail.com>
Sergey Ulanov <sergeyu@chromium.org>
S Hamsalekha <hamsalekha.s@ittiam.com>
Shimon Doodkin <helpmepro1@gmail.com>
Shunyao Li <shunyaoli@google.com>
SmilingWolf <lupo996@gmail.com>
Soo-Chul Han <shan@vidyo.com>
Stanislav Vitvitskyy <vitvitskyy@google.com>
Stefan Holmer <holmer@google.com>
Steinar Midtskogen <stemidts@cisco.com>
Steve Lhomme <robux4@gmail.com>
Suman Sunkara <sunkaras@google.com>
Susanna D'Souza <susannad@google.com>
Taekhyun Kim <takim@nvidia.com>
Takanori MATSUURA <t.matsuu@gmail.com>
Takuto Ikuta <tikuta@google.com>
Tamar Levy <tamar.levy@intel.com>
Tao Bai <michaelbai@chromium.org>
Tarek AMARA <amatarek@justin.tv>
Tarundeep Singh <tarundeep.singh@ittiam.com>
Tero Rintaluoma <teror@google.com>
Thijs Vermeir <thijsvermeir@gmail.com>
Thomas Daede <tdaede@mozilla.com>
Thomas Davies Thomas <thdavies@cisco.com>
Tim Kopp <tkopp@google.com>
Timothy B. Terriberry <tterribe@xiph.org>
Timo Witte <timo.witte@gmail.com>
Todd Nguyen <toddnguyen@google.com>
Tom Anderson <thomasanderson@google.com>
Tom Finegan <tomfinegan@google.com>
Tristan Matthews <tmatth@videolan.org>
ttwu <ttwu@andestech.com>
Umang Saini <umang.saini@ittiam.com>
Urvang Joshi <urvang@google.com>
Venkat Sanampudi <sanampudi.venkatarao@ittiam.com>
Victoria Zhislina <niva213@gmail.com>
Vignesh Venkatasubramanian <vigneshv@google.com>
Vikas Prasad <vikas.prasad@ittiam.com>
Vincent Rabaud <vrabaud@google.com>
Vishesh <vishesh.garg@ittiam.com>
Vishnu Teja Manyam <vishnu.teja@ittiam.com>
Vitalii Dziumenko <vdziumenko@luxoft.com>
Wan-Teh Chang <wtc@google.com>
Wei-Ting Lin <weitinglin@google.com>
Wenyao Liu <wenyao.liu@cidana.com>
Will Bresnahan <bill.wresnahan@gmail.com>
Xiaoqing Zhu <xzhu@netflix.com>
Xing Jin <ddvfinite@gmail.com>
Xin Zhao <xinzzhao@tencent.com>
Yannis Guyon <yguyon@google.com>
Yaowu Xu <yaowu@google.com>
Yeqing Wu <yeqing_wu@apple.com>
Yi Luo <luoyi@google.com>
Yingying Ma <yingying.ma@intel.com>
Yongzhe Wang <yongzhe@google.com>
Yuan Tong <tongyuan200097@gmail.com>
Yu-Chen (Eric) Sun <ycsun@fb.com>
Yue Chen <yuec@google.com>
Yunqing Wang <yunqingwang@google.com>
Yury Gitman <yuryg@google.com>
Yushin Cho <ycho@mozilla.com>
Zhaoliang Ma <zhaoliang.ma@intel.com>
Zhijie Yang <zhijie.yang@broadcom.com>
Zhipin Deng <zhipin.deng@intel.com>
Zoe Liu <zoeliu@gmail.com>
```

### licenses/pillow-libaom/third_party/fastfeat/LICENSE

```text
Copyright (c) 2006, 2008 Edward Rosten
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:


	*Redistributions of source code must retain the above copyright
	 notice, this list of conditions and the following disclaimer.

	*Redistributions in binary form must reproduce the above copyright
	 notice, this list of conditions and the following disclaimer in the
	 documentation and/or other materials provided with the distribution.

	*Neither the name of the University of Cambridge nor the names of
	 its contributors may be used to endorse or promote products derived
	 from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libaom/third_party/highway/LICENSE-BSD3

```text
Copyright (c) The Highway Project Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1.  Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libaom/third_party/libwebm/LICENSE.TXT

```text
Copyright (c) 2010, Google Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libaom/third_party/libwebm/PATENTS.TXT

```text
Additional IP Rights Grant (Patents)
------------------------------------

"These implementations" means the copyrightable works that implement the WebM
codecs distributed by Google as part of the WebM Project.

Google hereby grants to you a perpetual, worldwide, non-exclusive, no-charge,
royalty-free, irrevocable (except as stated in this section) patent license to
make, have made, use, offer to sell, sell, import, transfer, and otherwise
run, modify and propagate the contents of these implementations of WebM, where
such license applies only to those patent claims, both currently owned by
Google and acquired in the future, licensable by Google that are necessarily
infringed by these implementations of WebM. This grant does not include claims
that would be infringed only as a consequence of further modification of these
implementations. If you or your agent or exclusive licensee institute or order
or agree to the institution of patent litigation or any other patent
enforcement activity against any entity (including a cross-claim or
counterclaim in a lawsuit) alleging that any of these implementations of WebM
or any code incorporated within any of these implementations of WebM
constitute direct or contributory patent infringement, or inducement of
patent infringement, then any patent rights granted to you under this License
for these implementations of WebM shall terminate as of the date such
litigation is filed.
```

### licenses/pillow-libaom/third_party/libyuv/LICENSE

```text
Copyright 2011 The LibYuv Project Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libaom/third_party/vector/LICENSE

```text
The MIT License (MIT)
Copyright (c) 2016 Peter Goldsborough

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

### licenses/pillow-libaom/third_party/x86inc/LICENSE

```text
Copyright (C) 2005-2012 x264 project

Authors: Loren Merritt <lorenm@u.washington.edu>
         Anton Mitrofanov <BugMaster@narod.ru>
         Jason Garrett-Glaser <darkshikari@gmail.com>
         Henrik Gramner <hengar-6@student.ltu.se>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

### licenses/pillow-libaom/third_party/x86inc/x86inc.asm

```text
;*****************************************************************************
;* x86inc.asm: x264asm abstraction layer
;*****************************************************************************
;* Copyright (C) 2005-2019 x264 project
;*
;* Authors: Loren Merritt <lorenm@u.washington.edu>
;*          Henrik Gramner <henrik@gramner.com>
;*          Anton Mitrofanov <BugMaster@narod.ru>
;*          Fiona Glaser <fiona@x264.com>
;*
;* Permission to use, copy, modify, and/or distribute this software for any
;* purpose with or without fee is hereby granted, provided that the above
;* copyright notice and this permission notice appear in all copies.
;*
;* THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
;* WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
;* MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
;* ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
;* WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
;* ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
;* OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
;*****************************************************************************

; This is a header file for the x264ASM assembly language, which uses
; NASM/YASM syntax combined with a large number of macros to provide easy
; abstraction between different calling conventions (x86_32, win64, linux64).
; It also has various other useful features to simplify writing the kind of
; DSP functions that are most often used in x264.

; Unlike the rest of x264, this file is available under an ISC license, as it
; has significant usefulness outside of x264 and we want it to be available
; to the largest audience possible.  Of course, if you modify it for your own
; purposes to add a new feature, we strongly encourage contributing a patch
; as this feature might be useful for others as well.  Send patches or ideas
; to x264-devel@videolan.org .

%include "config/aom_config.asm"

%ifndef private_prefix
    %define private_prefix aom
%endif

%ifndef public_prefix
    %define public_prefix private_prefix
%endif

%ifndef STACK_ALIGNMENT
    %if AOM_ARCH_X86_64
        %define STACK_ALIGNMENT 16
    %else
        %define STACK_ALIGNMENT 4
    %endif
%endif

%define WIN64  0
%define UNIX64 0
%if AOM_ARCH_X86_64
    %ifidn __OUTPUT_FORMAT__,win32
        %define WIN64  1
    %elifidn __OUTPUT_FORMAT__,win64
        %define WIN64  1
    %elifidn __OUTPUT_FORMAT__,x64
        %define WIN64  1
    %else
        %define UNIX64 1
    %endif
%endif

%define FORMAT_ELF 0
%define FORMAT_MACHO 0
%ifidn __OUTPUT_FORMAT__,elf
    %define FORMAT_ELF 1
%elifidn __OUTPUT_FORMAT__,elf32
    %define FORMAT_ELF 1
%elifidn __OUTPUT_FORMAT__,elf64
    %define FORMAT_ELF 1
%elifidn __OUTPUT_FORMAT__,macho
    %define FORMAT_MACHO 1
%elifidn __OUTPUT_FORMAT__,macho32
    %define FORMAT_MACHO 1
%elifidn __OUTPUT_FORMAT__,macho64
    %define FORMAT_MACHO 1
%endif

; Set PREFIX for libaom builds.
%if FORMAT_ELF
    %undef PREFIX
%elif WIN64
    %undef PREFIX
%else
    %define PREFIX
%endif

%ifdef PREFIX
    %define mangle(x) _ %+ x
%else
    %define mangle(x) x
%endif

; In some instances macho32 tables get misaligned when using .rodata.
; When looking at the disassembly it appears that the offset is either
; correct or consistently off by 90. Placing them in the .text section
; works around the issue. It appears to be specific to the way libaom
; handles the tables.
%macro SECTION_RODATA 0-1 16
    %ifidn __OUTPUT_FORMAT__,win32
        SECTION .rdata align=%1
    %elif WIN64
        SECTION .rdata align=%1
    %elifidn __OUTPUT_FORMAT__,macho32
        SECTION .text align=%1
        fakegot:
    %elifidn __OUTPUT_FORMAT__,aout
        SECTION .text
    %else
        SECTION .rodata align=%1
    %endif
%endmacro

; PIC macros from aom_ports/x86_abi_support.asm.
%ifidn __OUTPUT_FORMAT__,elf32
%define ABI_IS_32BIT 1
%elifidn __OUTPUT_FORMAT__,macho32
%define ABI_IS_32BIT 1
%elifidn __OUTPUT_FORMAT__,win32
%define ABI_IS_32BIT 1
%elifidn __OUTPUT_FORMAT__,aout
%define ABI_IS_32BIT 1
%else
%define ABI_IS_32BIT 0
%endif

%if ABI_IS_32BIT
    %if CONFIG_PIC=1
        %ifidn __OUTPUT_FORMAT__,elf32
            %define GET_GOT_DEFINED 1
            %define WRT_PLT wrt ..plt
            %macro GET_GOT 1
                extern _GLOBAL_OFFSET_TABLE_
                push %1
                call %%get_got
                %%sub_offset:
                jmp %%exitGG
                %%get_got:
                mov %1, [esp]
                add %1, _GLOBAL_OFFSET_TABLE_ + $$ - %%sub_offset wrt ..gotpc
                ret
                %%exitGG:
                %undef GLOBAL
                %define GLOBAL(x) x + %1 wrt ..gotoff
                %undef RESTORE_GOT
                %define RESTORE_GOT pop %1
            %endmacro
        %elifidn __OUTPUT_FORMAT__,macho32
            %define GET_GOT_DEFINED 1
            %macro GET_GOT 1
                push %1
                call %%get_got
                %%get_got:
                pop  %1
                %undef GLOBAL
                %define GLOBAL(x) x + %1 - %%get_got
                %undef RESTORE_GOT
                %define RESTORE_GOT pop %1
            %endmacro
        %else
            %define GET_GOT_DEFINED 0
        %endif
    %endif

    %if AOM_ARCH_X86_64 == 0
        %undef PIC
    %endif

%else
    %macro GET_GOT 1
    %endmacro
    %define GLOBAL(x) rel x
    %define WRT_PLT wrt ..plt

    %if WIN64
        %define PIC
    %elifidn __OUTPUT_FORMAT__,macho64
        %define PIC
    %elif CONFIG_PIC
        %define PIC
    %endif
%endif

%ifnmacro GET_GOT
    %macro GET_GOT 1
    %endmacro
    %define GLOBAL(x) x
%endif
%ifndef RESTORE_GOT
    %define RESTORE_GOT
%endif
%ifndef WRT_PLT
    %define WRT_PLT
%endif

%ifdef PIC
    default rel
%endif

%ifndef GET_GOT_DEFINED
    %define GET_GOT_DEFINED 0
%endif
; End PIC macros from aom_ports/x86_abi_support.asm.

; libaom explicitly sets visibilty in shared object builds. Avoid setting
; visibility to hidden as it may break builds that split sources on e.g.,
; directory boundaries.
%ifdef CHROMIUM
    %define VISIBILITY hidden
    %define HAVE_PRIVATE_EXTERN 1
%else
    %define VISIBILITY
    %define HAVE_PRIVATE_EXTERN 0
%endif

%ifdef __NASM_VER__
    %use smartalign
    %if __NASM_VERSION_ID__ < 0x020e0000 ; 2.14
        %define HAVE_PRIVATE_EXTERN 0
    %endif
%endif

; Macros to eliminate most code duplication between x86_32 and x86_64:
; Currently this works only for leaf functions which load all their arguments
; into registers at the start, and make no other use of the stack. Luckily that
; covers most of x264's asm.

; PROLOGUE:
; %1 = number of arguments. loads them from stack if needed.
; %2 = number of registers used. pushes callee-saved regs if needed.
; %3 = number of xmm registers used. pushes callee-saved xmm regs if needed.
; %4 = (optional) stack size to be allocated. The stack will be aligned before
;      allocating the specified stack size. If the required stack alignment is
;      larger than the known stack alignment the stack will be manually aligned
;      and an extra register will be allocated to hold the original stack
;      pointer (to not invalidate r0m etc.). To prevent the use of an extra
;      register as stack pointer, request a negative stack size.
; %4+/%5+ = list of names to define to registers
; PROLOGUE can also be invoked by adding the same options to cglobal

; e.g.
; cglobal foo, 2,3,7,0x40, dst, src, tmp
; declares a function (foo) that automatically loads two arguments (dst and
; src) into registers, uses one additional register (tmp) plus 7 vector
; registers (m0-m6) and allocates 0x40 bytes of stack space.

; TODO Some functions can use some args directly from the stack. If they're the
; last args then you can just not declare them, but if they're in the middle
; we need more flexible macro.

; RET:
; Pops anything that was pushed by PROLOGUE, and returns.

; REP_RET:
; Use this instead of RET if it's a branch target.

; registers:
; rN and rNq are the native-size register holding function argument N
; rNd, rNw, rNb are dword, word, and byte size
; rNh is the high 8 bits of the word size
; rNm is the original location of arg N (a register or on the stack), dword
; rNmp is native size

%macro DECLARE_REG 2-3
    %define r%1q %2
    %define r%1d %2d
    %define r%1w %2w
    %define r%1b %2b
    %define r%1h %2h
    %define %2q %2
    %if %0 == 2
        %define r%1m  %2d
        %define r%1mp %2
    %elif AOM_ARCH_X86_64 ; memory
        %define r%1m [rstk + stack_offset + %3]
        %define r%1mp qword r %+ %1 %+ m
    %else
        %define r%1m [rstk + stack_offset + %3]
        %define r%1mp dword r %+ %1 %+ m
    %endif
    %define r%1  %2
%endmacro

%macro DECLARE_REG_SIZE 3
    %define r%1q r%1
    %define e%1q r%1
    %define r%1d e%1
    %define e%1d e%1
    %define r%1w %1
    %define e%1w %1
    %define r%1h %3
    %define e%1h %3
    %define r%1b %2
    %define e%1b %2
    %if AOM_ARCH_X86_64 == 0
        %define r%1 e%1
    %endif
%endmacro

DECLARE_REG_SIZE ax, al, ah
DECLARE_REG_SIZE bx, bl, bh
DECLARE_REG_SIZE cx, cl, ch
DECLARE_REG_SIZE dx, dl, dh
DECLARE_REG_SIZE si, sil, null
DECLARE_REG_SIZE di, dil, null
DECLARE_REG_SIZE bp, bpl, null

; t# defines for when per-arch register allocation is more complex than just function arguments

%macro DECLARE_REG_TMP 1-*
    %assign %%i 0
    %rep %0
        CAT_XDEFINE t, %%i, r%1
        %assign %%i %%i+1
        %rotate 1
    %endrep
%endmacro

%macro DECLARE_REG_TMP_SIZE 0-*
    %rep %0
        %define t%1q t%1 %+ q
        %define t%1d t%1 %+ d
        %define t%1w t%1 %+ w
        %define t%1h t%1 %+ h
        %define t%1b t%1 %+ b
        %rotate 1
    %endrep
%endmacro

DECLARE_REG_TMP_SIZE 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14

%if AOM_ARCH_X86_64
    %define gprsize 8
%else
    %define gprsize 4
%endif

%macro LEA 2
%if AOM_ARCH_X86_64
    lea %1, [%2]
%elif PIC
    call $+5 ; special-cased to not affect the RSB on most CPU:s
    pop %1
    add %1, (%2)-$+1
%else
    mov %1, %2
%endif
%endmacro

%macro PUSH 1
    push %1
    %ifidn rstk, rsp
        %assign stack_offset stack_offset+gprsize
    %endif
%endmacro

%macro POP 1
    pop %1
    %ifidn rstk, rsp
        %assign stack_offset stack_offset-gprsize
    %endif
%endmacro

%macro PUSH_IF_USED 1-*
    %rep %0
        %if %1 < regs_used
            PUSH r%1
        %endif
        %rotate 1
    %endrep
%endmacro

%macro POP_IF_USED 1-*
    %rep %0
        %if %1 < regs_used
            pop r%1
        %endif
        %rotate 1
    %endrep
%endmacro

%macro LOAD_IF_USED 1-*
    %rep %0
        %if %1 < num_args
            mov r%1, r %+ %1 %+ mp
        %endif
        %rotate 1
    %endrep
%endmacro

%macro SUB 2
    sub %1, %2
    %ifidn %1, rstk
        %assign stack_offset stack_offset+(%2)
    %endif
%endmacro

%macro ADD 2
    add %1, %2
    %ifidn %1, rstk
        %assign stack_offset stack_offset-(%2)
    %endif
%endmacro

%macro movifnidn 2
    %ifnidn %1, %2
        mov %1, %2
    %endif
%endmacro

%if AOM_ARCH_X86_64 == 0
    %define movsxd movifnidn
%endif

%macro movsxdifnidn 2
    %ifnidn %1, %2
        movsxd %1, %2
    %endif
%endmacro

%macro ASSERT 1
    %if (%1) == 0
        %error assertion ``%1'' failed
    %endif
%endmacro

%macro DEFINE_ARGS 0-*
    %ifdef n_arg_names
        %assign %%i 0
        %rep n_arg_names
            CAT_UNDEF arg_name %+ %%i, q
            CAT_UNDEF arg_name %+ %%i, d
            CAT_UNDEF arg_name %+ %%i, w
            CAT_UNDEF arg_name %+ %%i, h
            CAT_UNDEF arg_name %+ %%i, b
            CAT_UNDEF arg_name %+ %%i, m
            CAT_UNDEF arg_name %+ %%i, mp
            CAT_UNDEF arg_name, %%i
            %assign %%i %%i+1
        %endrep
    %endif

    %xdefine %%stack_offset stack_offset
    %undef stack_offset ; so that the current value of stack_offset doesn't get baked in by xdefine
    %assign %%i 0
    %rep %0
        %xdefine %1q r %+ %%i %+ q
        %xdefine %1d r %+ %%i %+ d
        %xdefine %1w r %+ %%i %+ w
        %xdefine %1h r %+ %%i %+ h
        %xdefine %1b r %+ %%i %+ b
        %xdefine %1m r %+ %%i %+ m
        %xdefine %1mp r %+ %%i %+ mp
        CAT_XDEFINE arg_name, %%i, %1
        %assign %%i %%i+1
        %rotate 1
    %endrep
    %xdefine stack_offset %%stack_offset
    %assign n_arg_names %0
%endmacro

%define required_stack_alignment ((mmsize + 15) & ~15)
%define vzeroupper_required (mmsize > 16 && (AOM_ARCH_X86_64 == 0 || xmm_regs_used > 16 || notcpuflag(avx512)))
%define high_mm_regs (16*cpuflag(avx512))

%macro ALLOC_STACK 1-2 0 ; stack_size, n_xmm_regs (for win64 only)
    %ifnum %1
        %if %1 != 0
            %assign %%pad 0
            %assign stack_size %1
            %if stack_size < 0
                %assign stack_size -stack_size
            %endif
            %if WIN64
                %assign %%pad %%pad + 32 ; shadow space
                %if mmsize != 8
                    %assign xmm_regs_used %2
                    %if xmm_regs_used > 8
                        %assign %%pad %%pad + (xmm_regs_used-8)*16 ; callee-saved xmm registers
                    %endif
                %endif
            %endif
            %if required_stack_alignment <= STACK_ALIGNMENT
                ; maintain the current stack alignment
                %assign stack_size_padded stack_size + %%pad + ((-%%pad-stack_offset-gprsize) & (STACK_ALIGNMENT-1))
                SUB rsp, stack_size_padded
            %else
                %assign %%reg_num (regs_used - 1)
                %xdefine rstk r %+ %%reg_num
                ; align stack, and save original stack location directly above
                ; it, i.e. in [rsp+stack_size_padded], so we can restore the
                ; stack in a single instruction (i.e. mov rsp, rstk or mov
                ; rsp, [rsp+stack_size_padded])
                %if %1 < 0 ; need to store rsp on stack
                    %xdefine rstkm [rsp + stack_size + %%pad]
                    %assign %%pad %%pad + gprsize
                %else ; can keep rsp in rstk during whole function
                    %xdefine rstkm rstk
                %endif
                %assign stack_size_padded stack_size + ((%%pad + required_stack_alignment-1) & ~(required_stack_alignment-1))
                mov rstk, rsp
                and rsp, ~(required_stack_alignment-1)
                sub rsp, stack_size_padded
                movifnidn rstkm, rstk
            %endif
            WIN64_PUSH_XMM
        %endif
    %endif
%endmacro

%macro SETUP_STACK_POINTER 1
    %ifnum %1
        %if %1 != 0 && required_stack_alignment > STACK_ALIGNMENT
            %if %1 > 0
                ; Reserve an additional register for storing the original stack pointer, but avoid using
                ; eax/rax for this purpose since it can potentially get overwritten as a return value.
                %assign regs_used (regs_used + 1)
                %if AOM_ARCH_X86_64 && regs_used == 7
                    %assign regs_used 8
                %elif AOM_ARCH_X86_64 == 0 && regs_used == 1
                    %assign regs_used 2
                %endif
            %endif
            %if AOM_ARCH_X86_64 && regs_used < 5 + UNIX64 * 3
                ; Ensure that we don't clobber any registers containing arguments. For UNIX64 we also preserve r6 (rax)
                ; since it's used as a hidden argument in vararg functions to specify the number of vector registers used.
                %assign regs_used 5 + UNIX64 * 3
            %endif
        %endif
    %endif
%endmacro

%macro DEFINE_ARGS_INTERNAL 3+
    %ifnum %2
        DEFINE_ARGS %3
    %elif %1 == 4
        DEFINE_ARGS %2
    %elif %1 > 4
        DEFINE_ARGS %2, %3
    %endif
%endmacro

%if WIN64 ; Windows x64 ;=================================================

DECLARE_REG 0,  rcx
DECLARE_REG 1,  rdx
DECLARE_REG 2,  R8
DECLARE_REG 3,  R9
DECLARE_REG 4,  R10, 40
DECLARE_REG 5,  R11, 48
DECLARE_REG 6,  rax, 56
DECLARE_REG 7,  rdi, 64
DECLARE_REG 8,  rsi, 72
DECLARE_REG 9,  rbx, 80
DECLARE_REG 10, rbp, 88
DECLARE_REG 11, R14, 96
DECLARE_REG 12, R15, 104
DECLARE_REG 13, R12, 112
DECLARE_REG 14, R13, 120

%macro PROLOGUE 2-5+ 0 ; #args, #regs, #xmm_regs, [stack_size,] arg_names...
    %assign num_args %1
    %assign regs_used %2
    ASSERT regs_used >= num_args
    SETUP_STACK_POINTER %4
    ASSERT regs_used <= 15
    PUSH_IF_USED 7, 8, 9, 10, 11, 12, 13, 14
    ALLOC_STACK %4, %3
    %if mmsize != 8 && stack_size == 0
        WIN64_SPILL_XMM %3
    %endif
    LOAD_IF_USED 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
    DEFINE_ARGS_INTERNAL %0, %4, %5
%endmacro

%macro WIN64_PUSH_XMM 0
    ; Use the shadow space to store XMM6 and XMM7, the rest needs stack space allocated.
    %if xmm_regs_used > 6 + high_mm_regs
        movaps [rstk + stack_offset +  8], xmm6
    %endif
    %if xmm_regs_used > 7 + high_mm_regs
        movaps [rstk + stack_offset + 24], xmm7
    %endif
    %assign %%xmm_regs_on_stack xmm_regs_used - high_mm_regs - 8
    %if %%xmm_regs_on_stack > 0
        %assign %%i 8
        %rep %%xmm_regs_on_stack
            movaps [rsp + (%%i-8)*16 + stack_size + 32], xmm %+ %%i
            %assign %%i %%i+1
        %endrep
    %endif
%endmacro

%macro WIN64_SPILL_XMM 1
    %assign xmm_regs_used %1
    ASSERT xmm_regs_used <= 16 + high_mm_regs
    %assign %%xmm_regs_on_stack xmm_regs_used - high_mm_regs - 8
    %if %%xmm_regs_on_stack > 0
        ; Allocate stack space for callee-saved xmm registers plus shadow space and align the stack.
        %assign %%pad %%xmm_regs_on_stack*16 + 32
        %assign stack_size_padded %%pad + ((-%%pad-stack_offset-gprsize) & (STACK_ALIGNMENT-1))
        SUB rsp, stack_size_padded
    %endif
    WIN64_PUSH_XMM
%endmacro

%macro WIN64_RESTORE_XMM_INTERNAL 0
    %assign %%pad_size 0
    %assign %%xmm_regs_on_stack xmm_regs_used - high_mm_regs - 8
    %if %%xmm_regs_on_stack > 0
        %assign %%i xmm_regs_used - high_mm_regs
        %rep %%xmm_regs_on_stack
            %assign %%i %%i-1
            movaps xmm %+ %%i, [rsp + (%%i-8)*16 + stack_size + 32]
        %endrep
    %endif
    %if stack_size_padded > 0
        %if stack_size > 0 && required_stack_alignment > STACK_ALIGNMENT
            mov rsp, rstkm
        %else
            add rsp, stack_size_padded
            %assign %%pad_size stack_size_padded
        %endif
    %endif
    %if xmm_regs_used > 7 + high_mm_regs
        movaps xmm7, [rsp + stack_offset - %%pad_size + 24]
    %endif
    %if xmm_regs_used > 6 + high_mm_regs
        movaps xmm6, [rsp + stack_offset - %%pad_size +  8]
    %endif
%endmacro

%macro WIN64_RESTORE_XMM 0
    WIN64_RESTORE_XMM_INTERNAL
    %assign stack_offset (stack_offset-stack_size_padded)
    %assign stack_size_padded 0
    %assign xmm_regs_used 0
%endmacro

%define has_epilogue regs_used > 7 || stack_size > 0 || vzeroupper_required || xmm_regs_used > 6+high_mm_regs

%macro RET 0
    WIN64_RESTORE_XMM_INTERNAL
    POP_IF_USED 14, 13, 12, 11, 10, 9, 8, 7
    %if vzeroupper_required
        vzeroupper
    %endif
    AUTO_REP_RET
%endmacro

%elif AOM_ARCH_X86_64 ; *nix x64 ;=============================================

DECLARE_REG 0,  rdi
DECLARE_REG 1,  rsi
DECLARE_REG 2,  rdx
DECLARE_REG 3,  rcx
DECLARE_REG 4,  R8
DECLARE_REG 5,  R9
DECLARE_REG 6,  rax, 8
DECLARE_REG 7,  R10, 16
DECLARE_REG 8,  R11, 24
DECLARE_REG 9,  rbx, 32
DECLARE_REG 10, rbp, 40
DECLARE_REG 11, R14, 48
DECLARE_REG 12, R15, 56
DECLARE_REG 13, R12, 64
DECLARE_REG 14, R13, 72

%macro PROLOGUE 2-5+ 0 ; #args, #regs, #xmm_regs, [stack_size,] arg_names...
    %assign num_args %1
    %assign regs_used %2
    %assign xmm_regs_used %3
    ASSERT regs_used >= num_args
    SETUP_STACK_POINTER %4
    ASSERT regs_used <= 15
    PUSH_IF_USED 9, 10, 11, 12, 13, 14
    ALLOC_STACK %4
    LOAD_IF_USED 6, 7, 8, 9, 10, 11, 12, 13, 14
    DEFINE_ARGS_INTERNAL %0, %4, %5
%endmacro

%define has_epilogue regs_used > 9 || stack_size > 0 || vzeroupper_required

%macro RET 0
    %if stack_size_padded > 0
        %if required_stack_alignment > STACK_ALIGNMENT
            mov rsp, rstkm
        %else
            add rsp, stack_size_padded
        %endif
    %endif
    POP_IF_USED 14, 13, 12, 11, 10, 9
    %if vzeroupper_required
        vzeroupper
    %endif
    AUTO_REP_RET
%endmacro

%else ; X86_32 ;==============================================================

DECLARE_REG 0, eax, 4
DECLARE_REG 1, ecx, 8
DECLARE_REG 2, edx, 12
DECLARE_REG 3, ebx, 16
DECLARE_REG 4, esi, 20
DECLARE_REG 5, edi, 24
DECLARE_REG 6, ebp, 28
%define rsp esp

%macro DECLARE_ARG 1-*
    %rep %0
        %define r%1m [rstk + stack_offset + 4*%1 + 4]
        %define r%1mp dword r%1m
        %rotate 1
    %endrep
%endmacro

DECLARE_ARG 7, 8, 9, 10, 11, 12, 13, 14

%macro PROLOGUE 2-5+ ; #args, #regs, #xmm_regs, [stack_size,] arg_names...
    %assign num_args %1
    %assign regs_used %2
    ASSERT regs_used >= num_args
    %if num_args > 7
        %assign num_args 7
    %endif
    %if regs_used > 7
        %assign regs_used 7
    %endif
    SETUP_STACK_POINTER %4
    ASSERT regs_used <= 7
    PUSH_IF_USED 3, 4, 5, 6
    ALLOC_STACK %4
    LOAD_IF_USED 0, 1, 2, 3, 4, 5, 6
    DEFINE_ARGS_INTERNAL %0, %4, %5
%endmacro

%define has_epilogue regs_used > 3 || stack_size > 0 || vzeroupper_required

%macro RET 0
    %if stack_size_padded > 0
        %if required_stack_alignment > STACK_ALIGNMENT
            mov rsp, rstkm
        %else
            add rsp, stack_size_padded
        %endif
    %endif
    POP_IF_USED 6, 5, 4, 3
    %if vzeroupper_required
        vzeroupper
    %endif
    AUTO_REP_RET
%endmacro

%endif ;======================================================================

%if WIN64 == 0
    %macro WIN64_SPILL_XMM 1
    %endmacro
    %macro WIN64_RESTORE_XMM 0
    %endmacro
    %macro WIN64_PUSH_XMM 0
    %endmacro
%endif

; On AMD cpus <=K10, an ordinary ret is slow if it immediately follows either
; a branch or a branch target. So switch to a 2-byte form of ret in that case.
; We can automatically detect "follows a branch", but not a branch target.
; (SSSE3 is a sufficient condition to know that your cpu doesn't have this problem.)
%macro REP_RET 0
    %if has_epilogue || cpuflag(ssse3)
        RET
    %else
        rep ret
    %endif
    annotate_function_size
%endmacro

%define last_branch_adr $$
%macro AUTO_REP_RET 0
    %if notcpuflag(ssse3)
        times ((last_branch_adr-$)>>31)+1 rep ; times 1 iff $ == last_branch_adr.
    %endif
    ret
    annotate_function_size
%endmacro

%macro BRANCH_INSTR 0-*
    %rep %0
        %macro %1 1-2 %1
            %2 %1
            %if notcpuflag(ssse3)
                %%branch_instr equ $
                %xdefine last_branch_adr %%branch_instr
            %endif
        %endmacro
        %rotate 1
    %endrep
%endmacro

BRANCH_INSTR jz, je, jnz, jne, jl, jle, jnl, jnle, jg, jge, jng, jnge, ja, jae, jna, jnae, jb, jbe, jnb, jnbe, jc, jnc, js, jns, jo, jno, jp, jnp

%macro TAIL_CALL 1-2 1 ; callee, is_nonadjacent
    %if has_epilogue
        call %1
        RET
    %elif %2
        jmp %1
    %endif
    annotate_function_size
%endmacro

;=============================================================================
; arch-independent part
;=============================================================================

%assign function_align 16

; Begin a function.
; Applies any symbol mangling needed for C linkage, and sets up a define such that
; subsequent uses of the function name automatically refer to the mangled version.
; Appends cpuflags to the function name if cpuflags has been specified.
; The "" empty default parameter is a workaround for nasm, which fails if SUFFIX
; is empty and we call cglobal_internal with just %1 %+ SUFFIX (without %2).
%macro cglobal 1-2+ "" ; name, [PROLOGUE args]
    cglobal_internal 1, %1 %+ SUFFIX, %2
%endmacro
%macro cvisible 1-2+ "" ; name, [PROLOGUE args]
    cglobal_internal 0, %1 %+ SUFFIX, %2
%endmacro
%macro cglobal_internal 2-3+
    annotate_function_size
    %ifndef cglobaled_%2
        %if %1
            %xdefine %2 mangle(private_prefix %+ _ %+ %2)
        %else
            %xdefine %2 mangle(public_prefix %+ _ %+ %2)
        %endif
        %xdefine %2.skip_prologue %2 %+ .skip_prologue
        CAT_XDEFINE cglobaled_, %2, 1
    %endif
    %xdefine current_function %2
    %xdefine current_function_section __SECT__
    %if FORMAT_ELF
        %if %1
            global %2:function VISIBILITY
        %else
            global %2:function
        %endif
    %elif FORMAT_MACHO && HAVE_PRIVATE_EXTERN && %1
        global %2:private_extern
    %else
        global %2
    %endif
    align function_align
    %2:
    RESET_MM_PERMUTATION        ; needed for x86-64, also makes disassembly somewhat nicer
    %xdefine rstk rsp           ; copy of the original stack pointer, used when greater alignment than the known stack alignment is required
    %assign stack_offset 0      ; stack pointer offset relative to the return address
    %assign stack_size 0        ; amount of stack space that can be freely used inside a function
    %assign stack_size_padded 0 ; total amount of allocated stack space, including space for callee-saved xmm registers on WIN64 and alignment padding
    %assign xmm_regs_used 0     ; number of XMM registers requested, used for dealing with callee-saved registers on WIN64 and vzeroupper
    %ifnidn %3, ""
        PROLOGUE %3
    %endif
%endmacro

; Create a global symbol from a local label with the correct name mangling and type
%macro cglobal_label 1
    %if FORMAT_ELF
        global current_function %+ %1:function VISIBILITY
    %elif FORMAT_MACHO && HAVE_PRIVATE_EXTERN
        global current_function %+ %1:private_extern
    %else
        global current_function %+ %1
    %endif
    %1:
%endmacro

%macro cextern 1
    %xdefine %1 mangle(private_prefix %+ _ %+ %1)
    CAT_XDEFINE cglobaled_, %1, 1
    extern %1
%endmacro

; like cextern, but without the prefix
%macro cextern_naked 1
    %ifdef PREFIX
        %xdefine %1 mangle(%1)
    %endif
    CAT_XDEFINE cglobaled_, %1, 1
    extern %1
%endmacro

%macro const 1-2+
    %xdefine %1 mangle(private_prefix %+ _ %+ %1)
    %if FORMAT_ELF
        global %1:data VISIBILITY
    %elif FORMAT_MACHO && HAVE_PRIVATE_EXTERN
        global %1:private_extern
    %else
        global %1
    %endif
    %1: %2
%endmacro

; This is needed for ELF, otherwise the GNU linker assumes the stack is executable by default.
%if FORMAT_ELF
    [SECTION .note.GNU-stack noalloc noexec nowrite progbits]
%endif

; Tell debuggers how large the function was.
; This may be invoked multiple times per function; we rely on later instances overriding earlier ones.
; This is invoked by RET and similar macros, and also cglobal does it for the previous function,
; but if the last function in a source file doesn't use any of the standard macros for its epilogue,
; then its size might be unspecified.
%macro annotate_function_size 0
    %ifdef __YASM_VER__
        %ifdef current_function
            %if FORMAT_ELF
                current_function_section
                %%ecf equ $
                size current_function %%ecf - current_function
                __SECT__
            %endif
        %endif
    %endif
%endmacro

; cpuflags

%assign cpuflags_mmx      (1<<0)
%assign cpuflags_mmx2     (1<<1) | cpuflags_mmx
%assign cpuflags_3dnow    (1<<2) | cpuflags_mmx
%assign cpuflags_3dnowext (1<<3) | cpuflags_3dnow
%assign cpuflags_sse      (1<<4) | cpuflags_mmx2
%assign cpuflags_sse2     (1<<5) | cpuflags_sse
%assign cpuflags_sse2slow (1<<6) | cpuflags_sse2
%assign cpuflags_lzcnt    (1<<7) | cpuflags_sse2
%assign cpuflags_sse3     (1<<8) | cpuflags_sse2
%assign cpuflags_ssse3    (1<<9) | cpuflags_sse3
%assign cpuflags_sse4     (1<<10)| cpuflags_ssse3
%assign cpuflags_sse42    (1<<11)| cpuflags_sse4
%assign cpuflags_aesni    (1<<12)| cpuflags_sse42
%assign cpuflags_gfni     (1<<13)| cpuflags_sse42
%assign cpuflags_avx      (1<<14)| cpuflags_sse42
%assign cpuflags_xop      (1<<15)| cpuflags_avx
%assign cpuflags_fma4     (1<<16)| cpuflags_avx
%assign cpuflags_fma3     (1<<17)| cpuflags_avx
%assign cpuflags_bmi1     (1<<18)| cpuflags_avx|cpuflags_lzcnt
%assign cpuflags_bmi2     (1<<19)| cpuflags_bmi1
%assign cpuflags_avx2     (1<<20)| cpuflags_fma3|cpuflags_bmi2
%assign cpuflags_avx512   (1<<21)| cpuflags_avx2 ; F, CD, BW, DQ, VL

%assign cpuflags_cache32  (1<<22)
%assign cpuflags_cache64  (1<<23)
%assign cpuflags_aligned  (1<<24) ; not a cpu feature, but a function variant
%assign cpuflags_atom     (1<<25)

; Returns a boolean value expressing whether or not the specified cpuflag is enabled.
%define    cpuflag(x) (((((cpuflags & (cpuflags_ %+ x)) ^ (cpuflags_ %+ x)) - 1) >> 31) & 1)
%define notcpuflag(x) (cpuflag(x) ^ 1)

; Takes an arbitrary number of cpuflags from the above list.
; All subsequent functions (up to the next INIT_CPUFLAGS) is built for the specified cpu.
; You shouldn't need to invoke this macro directly, it's a subroutine for INIT_MMX &co.
%macro INIT_CPUFLAGS 0-*
    %xdefine SUFFIX
    %undef cpuname
    %assign cpuflags 0

    %if %0 >= 1
        %rep %0
            %ifdef cpuname
                %xdefine cpuname cpuname %+ _%1
            %else
                %xdefine cpuname %1
            %endif
            %assign cpuflags cpuflags | cpuflags_%1
            %rotate 1
        %endrep
        %xdefine SUFFIX _ %+ cpuname

        %if cpuflag(avx)
            %assign avx_enabled 1
        %endif
        %if (mmsize == 16 && notcpuflag(sse2)) || (mmsize == 32 && notcpuflag(avx2))
            %define mova movaps
            %define movu movups
            %define movnta movntps
        %endif
        %if cpuflag(aligned)
            %define movu mova
        %elif cpuflag(sse3) && notcpuflag(ssse3)
            %define movu lddqu
        %endif
    %endif

    %if AOM_ARCH_X86_64 || cpuflag(sse2)
        %ifdef __NASM_VER__
            ALIGNMODE p6
        %else
            CPU amdnop
        %endif
    %else
        %ifdef __NASM_VER__
            ALIGNMODE nop
        %else
            CPU basicnop
        %endif
    %endif
%endmacro

; Merge mmx, sse*, and avx*
; m# is a simd register of the currently selected size
; xm# is the corresponding xmm register if mmsize >= 16, otherwise the same as m#
; ym# is the corresponding ymm register if mmsize >= 32, otherwise the same as m#
; zm# is the corresponding zmm register if mmsize >= 64, otherwise the same as m#
; (All 4 remain in sync through SWAP.)

%macro CAT_XDEFINE 3
    %xdefine %1%2 %3
%endmacro

%macro CAT_UNDEF 2
    %undef %1%2
%endmacro

%macro DEFINE_MMREGS 1 ; mmtype
    %assign %%prev_mmregs 0
    %ifdef num_mmregs
        %assign %%prev_mmregs num_mmregs
    %endif

    %assign num_mmregs 8
    %if AOM_ARCH_X86_64 && mmsize >= 16
        %assign num_mmregs 16
        %if cpuflag(avx512) || mmsize == 64
            %assign num_mmregs 32
        %endif
    %endif

    %assign %%i 0
    %rep num_mmregs
        CAT_XDEFINE m, %%i, %1 %+ %%i
        CAT_XDEFINE nn%1, %%i, %%i
        %assign %%i %%i+1
    %endrep
    %if %%prev_mmregs > num_mmregs
        %rep %%prev_mmregs - num_mmregs
            CAT_UNDEF m, %%i
            CAT_UNDEF nn %+ mmtype, %%i
            %assign %%i %%i+1
        %endrep
    %endif
    %xdefine mmtype %1
%endmacro

; Prefer registers 16-31 over 0-15 to avoid having to use vzeroupper
%macro AVX512_MM_PERMUTATION 0-1 0 ; start_reg
    %if AOM_ARCH_X86_64 && cpuflag(avx512)
        %assign %%i %1
        %rep 16-%1
            %assign %%i_high %%i+16
            SWAP %%i, %%i_high
            %assign %%i %%i+1
        %endrep
    %endif
%endmacro

%macro INIT_MMX 0-1+
    %assign avx_enabled 0
    %define RESET_MM_PERMUTATION INIT_MMX %1
    %define mmsize 8
    %define mova movq
    %define movu movq
    %define movh movd
    %define movnta movntq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS mm
%endmacro

%macro INIT_XMM 0-1+
    %assign avx_enabled 0
    %define RESET_MM_PERMUTATION INIT_XMM %1
    %define mmsize 16
    %define mova movdqa
    %define movu movdqu
    %define movh movq
    %define movnta movntdq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS xmm
    %if WIN64
        AVX512_MM_PERMUTATION 6 ; Swap callee-saved registers with volatile registers
    %endif
%endmacro

%macro INIT_YMM 0-1+
    %assign avx_enabled 1
    %define RESET_MM_PERMUTATION INIT_YMM %1
    %define mmsize 32
    %define mova movdqa
    %define movu movdqu
    %undef movh
    %define movnta movntdq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS ymm
    AVX512_MM_PERMUTATION
%endmacro

%macro INIT_ZMM 0-1+
    %assign avx_enabled 1
    %define RESET_MM_PERMUTATION INIT_ZMM %1
    %define mmsize 64
    %define mova movdqa
    %define movu movdqu
    %undef movh
    %define movnta movntdq
    INIT_CPUFLAGS %1
    DEFINE_MMREGS zmm
    AVX512_MM_PERMUTATION
%endmacro

INIT_XMM

%macro DECLARE_MMCAST 1
    %define  mmmm%1   mm%1
    %define  mmxmm%1  mm%1
    %define  mmymm%1  mm%1
    %define  mmzmm%1  mm%1
    %define xmmmm%1   mm%1
    %define xmmxmm%1 xmm%1
    %define xmmymm%1 xmm%1
    %define xmmzmm%1 xmm%1
    %define ymmmm%1   mm%1
    %define ymmxmm%1 xmm%1
    %define ymmymm%1 ymm%1
    %define ymmzmm%1 ymm%1
    %define zmmmm%1   mm%1
    %define zmmxmm%1 xmm%1
    %define zmmymm%1 ymm%1
    %define zmmzmm%1 zmm%1
    %define xm%1 xmm %+ m%1
    %define ym%1 ymm %+ m%1
    %define zm%1 zmm %+ m%1
%endmacro

%assign i 0
%rep 32
    DECLARE_MMCAST i
    %assign i i+1
%endrep

; I often want to use macros that permute their arguments. e.g. there's no
; efficient way to implement butterfly or transpose or dct without swapping some
; arguments.
;
; I would like to not have to manually keep track of the permutations:
; If I insert a permutation in the middle of a function, it should automatically
; change everything that follows. For more complex macros I may also have multiple
; implementations, e.g. the SSE2 and SSSE3 versions may have different permutations.
;
; Hence these macros. Insert a PERMUTE or some SWAPs at the end of a macro that
; permutes its arguments. It's equivalent to exchanging the contents of the
; registers, except that this way you exchange the register names instead, so it
; doesn't cost any cycles.

%macro PERMUTE 2-* ; takes a list of pairs to swap
    %rep %0/2
        %xdefine %%tmp%2 m%2
        %rotate 2
    %endrep
    %rep %0/2
        %xdefine m%1 %%tmp%2
        CAT_XDEFINE nn, m%1, %1
        %rotate 2
    %endrep
%endmacro

%macro SWAP 2+ ; swaps a single chain (sometimes more concise than pairs)
    %ifnum %1 ; SWAP 0, 1, ...
        SWAP_INTERNAL_NUM %1, %2
    %else ; SWAP m0, m1, ...
        SWAP_INTERNAL_NAME %1, %2
    %endif
%endmacro

%macro SWAP_INTERNAL_NUM 2-*
    %rep %0-1
        %xdefine %%tmp m%1
        %xdefine m%1 m%2
        %xdefine m%2 %%tmp
        CAT_XDEFINE nn, m%1, %1
        CAT_XDEFINE nn, m%2, %2
        %rotate 1
    %endrep
%endmacro

%macro SWAP_INTERNAL_NAME 2-*
    %xdefine %%args nn %+ %1
    %rep %0-1
        %xdefine %%args %%args, nn %+ %2
        %rotate 1
    %endrep
    SWAP_INTERNAL_NUM %%args
%endmacro

; If SAVE_MM_PERMUTATION is placed at the end of a function, then any later
; calls to that function will automatically load the permutation, so values can
; be returned in mmregs.
%macro SAVE_MM_PERMUTATION 0-1
    %if %0
        %xdefine %%f %1_m
    %else
        %xdefine %%f current_function %+ _m
    %endif
    %assign %%i 0
    %rep num_mmregs
        %xdefine %%tmp m %+ %%i
        CAT_XDEFINE %%f, %%i, regnumof %+ %%tmp
        %assign %%i %%i+1
    %endrep
%endmacro

%macro LOAD_MM_PERMUTATION 0-1 ; name to load from
    %if %0
        %xdefine %%f %1_m
    %else
        %xdefine %%f current_function %+ _m
    %endif
    %xdefine %%tmp %%f %+ 0
    %ifnum %%tmp
        RESET_MM_PERMUTATION
        %assign %%i 0
        %rep num_mmregs
            %xdefine %%tmp %%f %+ %%i
            CAT_XDEFINE %%m, %%i, m %+ %%tmp
            %assign %%i %%i+1
        %endrep
        %rep num_mmregs
            %assign %%i %%i-1
            CAT_XDEFINE m, %%i, %%m %+ %%i
            CAT_XDEFINE nn, m %+ %%i, %%i
        %endrep
    %endif
%endmacro

; Append cpuflags to the callee's name iff the appended name is known and the plain name isn't
%macro call 1
    %ifid %1
        call_internal %1 %+ SUFFIX, %1
    %else
        call %1
    %endif
%endmacro
%macro call_internal 2
    %xdefine %%i %2
    %ifndef cglobaled_%2
        %ifdef cglobaled_%1
            %xdefine %%i %1
        %endif
    %endif
    call %%i
    LOAD_MM_PERMUTATION %%i
%endmacro

; Substitutions that reduce instruction size but are functionally equivalent
%macro add 2
    %ifnum %2
        %if %2==128
            sub %1, -128
        %else
            add %1, %2
        %endif
    %else
        add %1, %2
    %endif
%endmacro

%macro sub 2
    %ifnum %2
        %if %2==128
            add %1, -128
        %else
            sub %1, %2
        %endif
    %else
        sub %1, %2
    %endif
%endmacro

;=============================================================================
; AVX abstraction layer
;=============================================================================

%assign i 0
%rep 32
    %if i < 8
        CAT_XDEFINE sizeofmm, i, 8
        CAT_XDEFINE regnumofmm, i, i
    %endif
    CAT_XDEFINE sizeofxmm, i, 16
    CAT_XDEFINE sizeofymm, i, 32
    CAT_XDEFINE sizeofzmm, i, 64
    CAT_XDEFINE regnumofxmm, i, i
    CAT_XDEFINE regnumofymm, i, i
    CAT_XDEFINE regnumofzmm, i, i
    %assign i i+1
%endrep
%undef i

%macro CHECK_AVX_INSTR_EMU 3-*
    %xdefine %%opcode %1
    %xdefine %%dst %2
    %rep %0-2
        %ifidn %%dst, %3
            %error non-avx emulation of ``%%opcode'' is not supported
        %endif
        %rotate 1
    %endrep
%endmacro

;%1 == instruction
;%2 == minimal instruction set
;%3 == 1 if float, 0 if int
;%4 == 1 if 4-operand emulation, 0 if 3-operand emulation, 255 otherwise (no emulation)
;%5 == 1 if commutative (i.e. doesn't matter which src arg is which), 0 if not
;%6+: operands
%macro RUN_AVX_INSTR 6-9+
    %ifnum sizeof%7
        %assign __sizeofreg sizeof%7
    %elifnum sizeof%6
        %assign __sizeofreg sizeof%6
    %else
        %assign __sizeofreg mmsize
    %endif
    %assign __emulate_avx 0
    %if avx_enabled && __sizeofreg >= 16
        %xdefine __instr v%1
    %else
        %xdefine __instr %1
        %if %0 >= 8+%4
            %assign __emulate_avx 1
        %endif
    %endif
    %ifnidn %2, fnord
        %ifdef cpuname
            %if notcpuflag(%2)
                %error use of ``%1'' %2 instruction in cpuname function: current_function
            %elif %3 == 0 && __sizeofreg == 16 && notcpuflag(sse2)
                %error use of ``%1'' sse2 instruction in cpuname function: current_function
            %elif %3 == 0 && __sizeofreg == 32 && notcpuflag(avx2)
                %error use of ``%1'' avx2 instruction in cpuname function: current_function
            %elif __sizeofreg == 16 && notcpuflag(sse)
                %error use of ``%1'' sse instruction in cpuname function: current_function
            %elif __sizeofreg == 32 && notcpuflag(avx)
                %error use of ``%1'' avx instruction in cpuname function: current_function
            %elif __sizeofreg == 64 && notcpuflag(avx512)
                %error use of ``%1'' avx512 instruction in cpuname function: current_function
            %elifidn %1, pextrw ; special case because the base instruction is mmx2,
                %ifnid %6       ; but sse4 is required for memory operands
                    %if notcpuflag(sse4)
                        %error use of ``%1'' sse4 instruction in cpuname function: current_function
                    %endif
                %endif
            %endif
        %endif
    %endif

    %if __emulate_avx
        %xdefine __src1 %7
        %xdefine __src2 %8
        %if %5 && %4 == 0
            %ifnidn %6, %7
                %ifidn %6, %8
                    %xdefine __src1 %8
                    %xdefine __src2 %7
                %elifnnum sizeof%8
                    ; 3-operand AVX instructions with a memory arg can only have it in src2,
                    ; whereas SSE emulation prefers to have it in src1 (i.e. the mov).
                    ; So, if the instruction is commutative with a memory arg, swap them.
                    %xdefine __src1 %8
                    %xdefine __src2 %7
                %endif
            %endif
        %endif
        %ifnidn %6, __src1
            %if %0 >= 9
                CHECK_AVX_INSTR_EMU {%1 %6, %7, %8, %9}, %6, __src2, %9
            %else
                CHECK_AVX_INSTR_EMU {%1 %6, %7, %8}, %6, __src2
            %endif
            %if __sizeofreg == 8
                MOVQ %6, __src1
            %elif %3
                MOVAPS %6, __src1
            %else
                MOVDQA %6, __src1
            %endif
        %endif
        %if %0 >= 9
            %1 %6, __src2, %9
        %else
            %1 %6, __src2
        %endif
    %elif %0 >= 9
        __instr %6, %7, %8, %9
    %elif %0 == 8
        %if avx_enabled && %5
            %xdefine __src1 %7
            %xdefine __src2 %8
            %ifnum regnumof%7
                %ifnum regnumof%8
                    %if regnumof%7 < 8 && regnumof%8 >= 8 && regnumof%8 < 16 && sizeof%8 <= 32
                        ; Most VEX-encoded instructions require an additional byte to encode when
                        ; src2 is a high register (e.g. m8..15). If the instruction is commutative
                        ; we can swap src1 and src2 when doing so reduces the instruction length.
                        %xdefine __src1 %8
                        %xdefine __src2 %7
                    %endif
                %endif
            %endif
            __instr %6, __src1, __src2
        %else
            __instr %6, %7, %8
        %endif
    %elif %0 == 7
        %if avx_enabled && %5
            %xdefine __src1 %6
            %xdefine __src2 %7
            %ifnum regnumof%6
                %ifnum regnumof%7
                    %if regnumof%6 < 8 && regnumof%7 >= 8 && regnumof%7 < 16 && sizeof%7 <= 32
                        %xdefine __src1 %7
                        %xdefine __src2 %6
                    %endif
                %endif
            %endif
            __instr %6, __src1, __src2
        %else
            __instr %6, %7
        %endif
    %else
        __instr %6
    %endif
%endmacro

;%1 == instruction
;%2 == minimal instruction set
;%3 == 1 if float, 0 if int
;%4 == 1 if 4-operand emulation, 0 if 3-operand emulation, 255 otherwise (no emulation)
;%5 == 1 if commutative (i.e. doesn't matter which src arg is which), 0 if not
%macro AVX_INSTR 1-5 fnord, 0, 255, 0
    %macro %1 1-10 fnord, fnord, fnord, fnord, %1, %2, %3, %4, %5
        %ifidn %2, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1
        %elifidn %3, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2
        %elifidn %4, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2, %3
        %elifidn %5, fnord
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2, %3, %4
        %else
            RUN_AVX_INSTR %6, %7, %8, %9, %10, %1, %2, %3, %4, %5
        %endif
    %endmacro
%endmacro

; Instructions with both VEX/EVEX and legacy encodings
; Non-destructive instructions are written without parameters
AVX_INSTR addpd, sse2, 1, 0, 1
AVX_INSTR addps, sse, 1, 0, 1
AVX_INSTR addsd, sse2, 1, 0, 0
AVX_INSTR addss, sse, 1, 0, 0
AVX_INSTR addsubpd, sse3, 1, 0, 0
AVX_INSTR addsubps, sse3, 1, 0, 0
AVX_INSTR aesdec, aesni, 0, 0, 0
AVX_INSTR aesdeclast, aesni, 0, 0, 0
AVX_INSTR aesenc, aesni, 0, 0, 0
AVX_INSTR aesenclast, aesni, 0, 0, 0
AVX_INSTR aesimc, aesni
AVX_INSTR aeskeygenassist, aesni
AVX_INSTR andnpd, sse2, 1, 0, 0
AVX_INSTR andnps, sse, 1, 0, 0
AVX_INSTR andpd, sse2, 1, 0, 1
AVX_INSTR andps, sse, 1, 0, 1
AVX_INSTR blendpd, sse4, 1, 1, 0
AVX_INSTR blendps, sse4, 1, 1, 0
AVX_INSTR blendvpd, sse4 ; can't be emulated
AVX_INSTR blendvps, sse4 ; can't be emulated
AVX_INSTR cmpeqpd, sse2, 1, 0, 1
AVX_INSTR cmpeqps, sse, 1, 0, 1
AVX_INSTR cmpeqsd, sse2, 1, 0, 0
AVX_INSTR cmpeqss, sse, 1, 0, 0
AVX_INSTR cmplepd, sse2, 1, 0, 0
AVX_INSTR cmpleps, sse, 1, 0, 0
AVX_INSTR cmplesd, sse2, 1, 0, 0
AVX_INSTR cmpless, sse, 1, 0, 0
AVX_INSTR cmpltpd, sse2, 1, 0, 0
AVX_INSTR cmpltps, sse, 1, 0, 0
AVX_INSTR cmpltsd, sse2, 1, 0, 0
AVX_INSTR cmpltss, sse, 1, 0, 0
AVX_INSTR cmpneqpd, sse2, 1, 0, 1
AVX_INSTR cmpneqps, sse, 1, 0, 1
AVX_INSTR cmpneqsd, sse2, 1, 0, 0
AVX_INSTR cmpneqss, sse, 1, 0, 0
AVX_INSTR cmpnlepd, sse2, 1, 0, 0
AVX_INSTR cmpnleps, sse, 1, 0, 0
AVX_INSTR cmpnlesd, sse2, 1, 0, 0
AVX_INSTR cmpnless, sse, 1, 0, 0
AVX_INSTR cmpnltpd, sse2, 1, 0, 0
AVX_INSTR cmpnltps, sse, 1, 0, 0
AVX_INSTR cmpnltsd, sse2, 1, 0, 0
AVX_INSTR cmpnltss, sse, 1, 0, 0
AVX_INSTR cmpordpd, sse2 1, 0, 1
AVX_INSTR cmpordps, sse 1, 0, 1
AVX_INSTR cmpordsd, sse2 1, 0, 0
AVX_INSTR cmpordss, sse 1, 0, 0
AVX_INSTR cmppd, sse2, 1, 1, 0
AVX_INSTR cmpps, sse, 1, 1, 0
AVX_INSTR cmpsd, sse2, 1, 1, 0
AVX_INSTR cmpss, sse, 1, 1, 0
AVX_INSTR cmpunordpd, sse2, 1, 0, 1
AVX_INSTR cmpunordps, sse, 1, 0, 1
AVX_INSTR cmpunordsd, sse2, 1, 0, 0
AVX_INSTR cmpunordss, sse, 1, 0, 0
AVX_INSTR comisd, sse2, 1
AVX_INSTR comiss, sse, 1
AVX_INSTR cvtdq2pd, sse2, 1
AVX_INSTR cvtdq2ps, sse2, 1
AVX_INSTR cvtpd2dq, sse2, 1
AVX_INSTR cvtpd2ps, sse2, 1
AVX_INSTR cvtps2dq, sse2, 1
AVX_INSTR cvtps2pd, sse2, 1
AVX_INSTR cvtsd2si, sse2, 1
AVX_INSTR cvtsd2ss, sse2, 1, 0, 0
AVX_INSTR cvtsi2sd, sse2, 1, 0, 0
AVX_INSTR cvtsi2ss, sse, 1, 0, 0
AVX_INSTR cvtss2sd, sse2, 1, 0, 0
AVX_INSTR cvtss2si, sse, 1
AVX_INSTR cvttpd2dq, sse2, 1
AVX_INSTR cvttps2dq, sse2, 1
AVX_INSTR cvttsd2si, sse2, 1
AVX_INSTR cvttss2si, sse, 1
AVX_INSTR divpd, sse2, 1, 0, 0
AVX_INSTR divps, sse, 1, 0, 0
AVX_INSTR divsd, sse2, 1, 0, 0
AVX_INSTR divss, sse, 1, 0, 0
AVX_INSTR dppd, sse4, 1, 1, 0
AVX_INSTR dpps, sse4, 1, 1, 0
AVX_INSTR extractps, sse4, 1
AVX_INSTR gf2p8affineinvqb, gfni, 0, 1, 0
AVX_INSTR gf2p8affineqb, gfni, 0, 1, 0
AVX_INSTR gf2p8mulb, gfni, 0, 0, 0
AVX_INSTR haddpd, sse3, 1, 0, 0
AVX_INSTR haddps, sse3, 1, 0, 0
AVX_INSTR hsubpd, sse3, 1, 0, 0
AVX_INSTR hsubps, sse3, 1, 0, 0
AVX_INSTR insertps, sse4, 1, 1, 0
AVX_INSTR lddqu, sse3
AVX_INSTR ldmxcsr, sse, 1
AVX_INSTR maskmovdqu, sse2
AVX_INSTR maxpd, sse2, 1, 0, 1
AVX_INSTR maxps, sse, 1, 0, 1
AVX_INSTR maxsd, sse2, 1, 0, 0
AVX_INSTR maxss, sse, 1, 0, 0
AVX_INSTR minpd, sse2, 1, 0, 1
AVX_INSTR minps, sse, 1, 0, 1
AVX_INSTR minsd, sse2, 1, 0, 0
AVX_INSTR minss, sse, 1, 0, 0
AVX_INSTR movapd, sse2, 1
AVX_INSTR movaps, sse, 1
AVX_INSTR movd, mmx
AVX_INSTR movddup, sse3, 1
AVX_INSTR movdqa, sse2
AVX_INSTR movdqu, sse2
AVX_INSTR movhlps, sse, 1, 0, 0
AVX_INSTR movhpd, sse2, 1, 0, 0
AVX_INSTR movhps, sse, 1, 0, 0
AVX_INSTR movlhps, sse, 1, 0, 0
AVX_INSTR movlpd, sse2, 1, 0, 0
AVX_INSTR movlps, sse, 1, 0, 0
AVX_INSTR movmskpd, sse2, 1
AVX_INSTR movmskps, sse, 1
AVX_INSTR movntdq, sse2
AVX_INSTR movntdqa, sse4
AVX_INSTR movntpd, sse2, 1
AVX_INSTR movntps, sse, 1
AVX_INSTR movq, mmx
AVX_INSTR movsd, sse2, 1, 0, 0
AVX_INSTR movshdup, sse3, 1
AVX_INSTR movsldup, sse3, 1
AVX_INSTR movss, sse, 1, 0, 0
AVX_INSTR movupd, sse2, 1
AVX_INSTR movups, sse, 1
AVX_INSTR mpsadbw, sse4, 0, 1, 0
AVX_INSTR mulpd, sse2, 1, 0, 1
AVX_INSTR mulps, sse, 1, 0, 1
AVX_INSTR mulsd, sse2, 1, 0, 0
AVX_INSTR mulss, sse, 1, 0, 0
AVX_INSTR orpd, sse2, 1, 0, 1
AVX_INSTR orps, sse, 1, 0, 1
AVX_INSTR pabsb, ssse3
AVX_INSTR pabsd, ssse3
AVX_INSTR pabsw, ssse3
AVX_INSTR packsswb, mmx, 0, 0, 0
AVX_INSTR packssdw, mmx, 0, 0, 0
AVX_INSTR packuswb, mmx, 0, 0, 0
AVX_INSTR packusdw, sse4, 0, 0, 0
AVX_INSTR paddb, mmx, 0, 0, 1
AVX_INSTR paddw, mmx, 0, 0, 1
AVX_INSTR paddd, mmx, 0, 0, 1
AVX_INSTR paddq, sse2, 0, 0, 1
AVX_INSTR paddsb, mmx, 0, 0, 1
AVX_INSTR paddsw, mmx, 0, 0, 1
AVX_INSTR paddusb, mmx, 0, 0, 1
AVX_INSTR paddusw, mmx, 0, 0, 1
AVX_INSTR palignr, ssse3, 0, 1, 0
AVX_INSTR pand, mmx, 0, 0, 1
AVX_INSTR pandn, mmx, 0, 0, 0
AVX_INSTR pavgb, mmx2, 0, 0, 1
AVX_INSTR pavgw, mmx2, 0, 0, 1
AVX_INSTR pblendvb, sse4 ; can't be emulated
AVX_INSTR pblendw, sse4, 0, 1, 0
AVX_INSTR pclmulqdq, fnord, 0, 1, 0
AVX_INSTR pclmulhqhqdq, fnord, 0, 0, 0
AVX_INSTR pclmulhqlqdq, fnord, 0, 0, 0
AVX_INSTR pclmullqhqdq, fnord, 0, 0, 0
AVX_INSTR pclmullqlqdq, fnord, 0, 0, 0
AVX_INSTR pcmpestri, sse42
AVX_INSTR pcmpestrm, sse42
AVX_INSTR pcmpistri, sse42
AVX_INSTR pcmpistrm, sse42
AVX_INSTR pcmpeqb, mmx, 0, 0, 1
AVX_INSTR pcmpeqw, mmx, 0, 0, 1
AVX_INSTR pcmpeqd, mmx, 0, 0, 1
AVX_INSTR pcmpeqq, sse4, 0, 0, 1
AVX_INSTR pcmpgtb, mmx, 0, 0, 0
AVX_INSTR pcmpgtw, mmx, 0, 0, 0
AVX_INSTR pcmpgtd, mmx, 0, 0, 0
AVX_INSTR pcmpgtq, sse42, 0, 0, 0
AVX_INSTR pextrb, sse4
AVX_INSTR pextrd, sse4
AVX_INSTR pextrq, sse4
AVX_INSTR pextrw, mmx2
AVX_INSTR phaddw, ssse3, 0, 0, 0
AVX_INSTR phaddd, ssse3, 0, 0, 0
AVX_INSTR phaddsw, ssse3, 0, 0, 0
AVX_INSTR phminposuw, sse4
AVX_INSTR phsubw, ssse3, 0, 0, 0
AVX_INSTR phsubd, ssse3, 0, 0, 0
AVX_INSTR phsubsw, ssse3, 0, 0, 0
AVX_INSTR pinsrb, sse4, 0, 1, 0
AVX_INSTR pinsrd, sse4, 0, 1, 0
AVX_INSTR pinsrq, sse4, 0, 1, 0
AVX_INSTR pinsrw, mmx2, 0, 1, 0
AVX_INSTR pmaddwd, mmx, 0, 0, 1
AVX_INSTR pmaddubsw, ssse3, 0, 0, 0
AVX_INSTR pmaxsb, sse4, 0, 0, 1
AVX_INSTR pmaxsw, mmx2, 0, 0, 1
AVX_INSTR pmaxsd, sse4, 0, 0, 1
AVX_INSTR pmaxub, mmx2, 0, 0, 1
AVX_INSTR pmaxuw, sse4, 0, 0, 1
AVX_INSTR pmaxud, sse4, 0, 0, 1
AVX_INSTR pminsb, sse4, 0, 0, 1
AVX_INSTR pminsw, mmx2, 0, 0, 1
AVX_INSTR pminsd, sse4, 0, 0, 1
AVX_INSTR pminub, mmx2, 0, 0, 1
AVX_INSTR pminuw, sse4, 0, 0, 1
AVX_INSTR pminud, sse4, 0, 0, 1
AVX_INSTR pmovmskb, mmx2
AVX_INSTR pmovsxbw, sse4
AVX_INSTR pmovsxbd, sse4
AVX_INSTR pmovsxbq, sse4
AVX_INSTR pmovsxwd, sse4
AVX_INSTR pmovsxwq, sse4
AVX_INSTR pmovsxdq, sse4
AVX_INSTR pmovzxbw, sse4
AVX_INSTR pmovzxbd, sse4
AVX_INSTR pmovzxbq, sse4
AVX_INSTR pmovzxwd, sse4
AVX_INSTR pmovzxwq, sse4
AVX_INSTR pmovzxdq, sse4
AVX_INSTR pmuldq, sse4, 0, 0, 1
AVX_INSTR pmulhrsw, ssse3, 0, 0, 1
AVX_INSTR pmulhuw, mmx2, 0, 0, 1
AVX_INSTR pmulhw, mmx, 0, 0, 1
AVX_INSTR pmullw, mmx, 0, 0, 1
AVX_INSTR pmulld, sse4, 0, 0, 1
AVX_INSTR pmuludq, sse2, 0, 0, 1
AVX_INSTR por, mmx, 0, 0, 1
AVX_INSTR psadbw, mmx2, 0, 0, 1
AVX_INSTR pshufb, ssse3, 0, 0, 0
AVX_INSTR pshufd, sse2
AVX_INSTR pshufhw, sse2
AVX_INSTR pshuflw, sse2
AVX_INSTR psignb, ssse3, 0, 0, 0
AVX_INSTR psignw, ssse3, 0, 0, 0
AVX_INSTR psignd, ssse3, 0, 0, 0
AVX_INSTR psllw, mmx, 0, 0, 0
AVX_INSTR pslld, mmx, 0, 0, 0
AVX_INSTR psllq, mmx, 0, 0, 0
AVX_INSTR pslldq, sse2, 0, 0, 0
AVX_INSTR psraw, mmx, 0, 0, 0
AVX_INSTR psrad, mmx, 0, 0, 0
AVX_INSTR psrlw, mmx, 0, 0, 0
AVX_INSTR psrld, mmx, 0, 0, 0
AVX_INSTR psrlq, mmx, 0, 0, 0
AVX_INSTR psrldq, sse2, 0, 0, 0
AVX_INSTR psubb, mmx, 0, 0, 0
AVX_INSTR psubw, mmx, 0, 0, 0
AVX_INSTR psubd, mmx, 0, 0, 0
AVX_INSTR psubq, sse2, 0, 0, 0
AVX_INSTR psubsb, mmx, 0, 0, 0
AVX_INSTR psubsw, mmx, 0, 0, 0
AVX_INSTR psubusb, mmx, 0, 0, 0
AVX_INSTR psubusw, mmx, 0, 0, 0
AVX_INSTR ptest, sse4
AVX_INSTR punpckhbw, mmx, 0, 0, 0
AVX_INSTR punpckhwd, mmx, 0, 0, 0
AVX_INSTR punpckhdq, mmx, 0, 0, 0
AVX_INSTR punpckhqdq, sse2, 0, 0, 0
AVX_INSTR punpcklbw, mmx, 0, 0, 0
AVX_INSTR punpcklwd, mmx, 0, 0, 0
AVX_INSTR punpckldq, mmx, 0, 0, 0
AVX_INSTR punpcklqdq, sse2, 0, 0, 0
AVX_INSTR pxor, mmx, 0, 0, 1
AVX_INSTR rcpps, sse, 1
AVX_INSTR rcpss, sse, 1, 0, 0
AVX_INSTR roundpd, sse4, 1
AVX_INSTR roundps, sse4, 1
AVX_INSTR roundsd, sse4, 1, 1, 0
AVX_INSTR roundss, sse4, 1, 1, 0
AVX_INSTR rsqrtps, sse, 1
AVX_INSTR rsqrtss, sse, 1, 0, 0
AVX_INSTR shufpd, sse2, 1, 1, 0
AVX_INSTR shufps, sse, 1, 1, 0
AVX_INSTR sqrtpd, sse2, 1
AVX_INSTR sqrtps, sse, 1
AVX_INSTR sqrtsd, sse2, 1, 0, 0
AVX_INSTR sqrtss, sse, 1, 0, 0
AVX_INSTR stmxcsr, sse, 1
AVX_INSTR subpd, sse2, 1, 0, 0
AVX_INSTR subps, sse, 1, 0, 0
AVX_INSTR subsd, sse2, 1, 0, 0
AVX_INSTR subss, sse, 1, 0, 0
AVX_INSTR ucomisd, sse2, 1
AVX_INSTR ucomiss, sse, 1
AVX_INSTR unpckhpd, sse2, 1, 0, 0
AVX_INSTR unpckhps, sse, 1, 0, 0
AVX_INSTR unpcklpd, sse2, 1, 0, 0
AVX_INSTR unpcklps, sse, 1, 0, 0
AVX_INSTR xorpd, sse2, 1, 0, 1
AVX_INSTR xorps, sse, 1, 0, 1

; 3DNow instructions, for sharing code between AVX, SSE and 3DN
AVX_INSTR pfadd, 3dnow, 1, 0, 1
AVX_INSTR pfsub, 3dnow, 1, 0, 0
AVX_INSTR pfmul, 3dnow, 1, 0, 1

;%1 == instruction
;%2 == minimal instruction set
%macro GPR_INSTR 2
    %macro %1 2-5 fnord, %1, %2
        %ifdef cpuname
            %if notcpuflag(%5)
                %error use of ``%4'' %5 instruction in cpuname function: current_function
            %endif
        %endif
        %ifidn %3, fnord
            %4 %1, %2
        %else
            %4 %1, %2, %3
        %endif
    %endmacro
%endmacro

GPR_INSTR andn, bmi1
GPR_INSTR bextr, bmi1
GPR_INSTR blsi, bmi1
GPR_INSTR blsr, bmi1
GPR_INSTR blsmsk, bmi1
GPR_INSTR bzhi, bmi2
GPR_INSTR mulx, bmi2
GPR_INSTR pdep, bmi2
GPR_INSTR pext, bmi2
GPR_INSTR popcnt, sse42
GPR_INSTR rorx, bmi2
GPR_INSTR sarx, bmi2
GPR_INSTR shlx, bmi2
GPR_INSTR shrx, bmi2

; base-4 constants for shuffles
%assign i 0
%rep 256
    %assign j ((i>>6)&3)*1000 + ((i>>4)&3)*100 + ((i>>2)&3)*10 + (i&3)
    %if j < 10
        CAT_XDEFINE q000, j, i
    %elif j < 100
        CAT_XDEFINE q00, j, i
    %elif j < 1000
        CAT_XDEFINE q0, j, i
    %else
        CAT_XDEFINE q, j, i
    %endif
    %assign i i+1
%endrep
%undef i
%undef j

%macro FMA_INSTR 3
    %macro %1 4-7 %1, %2, %3
        %if cpuflag(xop)
            v%5 %1, %2, %3, %4
        %elifnidn %1, %4
            %6 %1, %2, %3
            %7 %1, %4
        %else
            %error non-xop emulation of ``%5 %1, %2, %3, %4'' is not supported
        %endif
    %endmacro
%endmacro

FMA_INSTR  pmacsww,  pmullw, paddw
FMA_INSTR  pmacsdd,  pmulld, paddd ; sse4 emulation
FMA_INSTR pmacsdql,  pmuldq, paddq ; sse4 emulation
FMA_INSTR pmadcswd, pmaddwd, paddd

; Macros for consolidating FMA3 and FMA4 using 4-operand (dst, src1, src2, src3) syntax.
; FMA3 is only possible if dst is the same as one of the src registers.
; Either src2 or src3 can be a memory operand.
%macro FMA4_INSTR 2-*
    %push fma4_instr
    %xdefine %$prefix %1
    %rep %0 - 1
        %macro %$prefix%2 4-6 %$prefix, %2
            %if notcpuflag(fma3) && notcpuflag(fma4)
                %error use of ``%5%6'' fma instruction in cpuname function: current_function
            %elif cpuflag(fma4)
                v%5%6 %1, %2, %3, %4
            %elifidn %1, %2
                ; If %3 or %4 is a memory operand it needs to be encoded as the last operand.
                %ifnum sizeof%3
                    v%{5}213%6 %2, %3, %4
                %else
                    v%{5}132%6 %2, %4, %3
                %endif
            %elifidn %1, %3
                v%{5}213%6 %3, %2, %4
            %elifidn %1, %4
                v%{5}231%6 %4, %2, %3
            %else
                %error fma3 emulation of ``%5%6 %1, %2, %3, %4'' is not supported
            %endif
        %endmacro
        %rotate 1
    %endrep
    %pop
%endmacro

FMA4_INSTR fmadd,    pd, ps, sd, ss
FMA4_INSTR fmaddsub, pd, ps
FMA4_INSTR fmsub,    pd, ps, sd, ss
FMA4_INSTR fmsubadd, pd, ps
FMA4_INSTR fnmadd,   pd, ps, sd, ss
FMA4_INSTR fnmsub,   pd, ps, sd, ss

; Macros for converting VEX instructions to equivalent EVEX ones.
%macro EVEX_INSTR 2-3 0 ; vex, evex, prefer_evex
    %macro %1 2-7 fnord, fnord, %1, %2, %3
        %ifidn %3, fnord
            %define %%args %1, %2
        %elifidn %4, fnord
            %define %%args %1, %2, %3
        %else
            %define %%args %1, %2, %3, %4
        %endif
        %assign %%evex_required cpuflag(avx512) & %7
        %ifnum regnumof%1
            %if regnumof%1 >= 16 || sizeof%1 > 32
                %assign %%evex_required 1
            %endif
        %endif
        %ifnum regnumof%2
            %if regnumof%2 >= 16 || sizeof%2 > 32
                %assign %%evex_required 1
            %endif
        %endif
        %ifnum regnumof%3
            %if regnumof%3 >= 16 || sizeof%3 > 32
                %assign %%evex_required 1
            %endif
        %endif
        %if %%evex_required
            %6 %%args
        %else
            %5 %%args ; Prefer VEX over EVEX due to shorter instruction length
        %endif
    %endmacro
%endmacro

EVEX_INSTR vbroadcastf128, vbroadcastf32x4
EVEX_INSTR vbroadcasti128, vbroadcasti32x4
EVEX_INSTR vextractf128,   vextractf32x4
EVEX_INSTR vextracti128,   vextracti32x4
EVEX_INSTR vinsertf128,    vinsertf32x4
EVEX_INSTR vinserti128,    vinserti32x4
EVEX_INSTR vmovdqa,        vmovdqa32
EVEX_INSTR vmovdqu,        vmovdqu32
EVEX_INSTR vpand,          vpandd
EVEX_INSTR vpandn,         vpandnd
EVEX_INSTR vpor,           vpord
EVEX_INSTR vpxor,          vpxord
EVEX_INSTR vrcpps,         vrcp14ps,   1 ; EVEX versions have higher precision
EVEX_INSTR vrcpss,         vrcp14ss,   1
EVEX_INSTR vrsqrtps,       vrsqrt14ps, 1
EVEX_INSTR vrsqrtss,       vrsqrt14ss, 1
```

## libavif — 1.4.2

License: BSD-2-Clause + incorporated notices

Upstream: https://github.com/AOMediaCodec/libavif

### licenses/pillow-libavif/LICENSE

```text
Copyright 2019 Joe Drago. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------------

Files: src/obu.c

Copyright © 2018-2019, VideoLAN and dav1d authors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------------

Files: third_party/iccjpeg/*

In plain English:

1. We don't promise that this software works.  (But if you find any bugs,
   please let us know!)
2. You can use this software for whatever you want.  You don't have to pay us.
3. You may not pretend that you wrote this software.  If you use it in a
   program, you must acknowledge somewhere in your documentation that
   you've used the IJG code.

In legalese:

The authors make NO WARRANTY or representation, either express or implied,
with respect to this software, its quality, accuracy, merchantability, or
fitness for a particular purpose.  This software is provided "AS IS", and you,
its user, assume the entire risk as to its quality and accuracy.

This software is copyright (C) 1991-2013, Thomas G. Lane, Guido Vollbeding.
All Rights Reserved except as specified below.

Permission is hereby granted to use, copy, modify, and distribute this
software (or portions thereof) for any purpose, without fee, subject to these
conditions:
(1) If any part of the source code for this software is distributed, then this
README file must be included, with this copyright and no-warranty notice
unaltered; and any additions, deletions, or changes to the original files
must be clearly indicated in accompanying documentation.
(2) If only executable code is distributed, then the accompanying
documentation must state that "this software is based in part on the work of
the Independent JPEG Group".
(3) Permission for use of this software is granted only if the user accepts
full responsibility for any undesirable consequences; the authors accept
NO LIABILITY for damages of any kind.

These conditions apply to any software derived from or based on the IJG code,
not just to the unmodified library.  If you use our work, you ought to
acknowledge us.

Permission is NOT granted for the use of any IJG author's name or company name
in advertising or publicity relating to this software or products derived from
it.  This software may be referred to only as "the Independent JPEG Group's
software".

We specifically permit and encourage the use of this software as the basis of
commercial products, provided that all warranty or liability claims are
assumed by the product vendor.


The Unix configuration script "configure" was produced with GNU Autoconf.
It is copyright by the Free Software Foundation but is freely distributable.
The same holds for its supporting scripts (config.guess, config.sub,
ltmain.sh).  Another support script, install-sh, is copyright by X Consortium
but is also freely distributable.

The IJG distribution formerly included code to read and write GIF files.
To avoid entanglement with the Unisys LZW patent, GIF reading support has
been removed altogether, and the GIF writer has been simplified to produce
"uncompressed GIFs".  This technique does not use the LZW algorithm; the
resulting GIF files are larger than usual, but are readable by all standard
GIF decoders.

We are required to state that
    "The Graphics Interchange Format(c) is the Copyright property of
    CompuServe Incorporated.  GIF(sm) is a Service Mark property of
    CompuServe Incorporated."

------------------------------------------------------------------------------

Files: contrib/gdk-pixbuf/*

Copyright 2020 Emmanuel Gil Peyrot. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------------

Files: android_jni/gradlew*


                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

------------------------------------------------------------------------------

Files: third_party/libyuv/*

Copyright 2011 The LibYuv Project Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## libjpeg-turbo — 3.2.0

License: BSD-3-Clause AND IJG AND Zlib

Upstream: https://github.com/libjpeg-turbo/libjpeg-turbo

### licenses/pillow-libjpeg-turbo/LICENSE.md

```text
libjpeg-turbo Licenses
======================

libjpeg-turbo is covered by two compatible BSD-style open source licenses:

- The IJG (Independent JPEG Group) License, which is listed in
  [README.ijg](README.ijg)

  This license applies to the libjpeg API library and associated programs,
  including any code inherited from libjpeg and any modifications to that
  code.

- The Modified (3-clause) BSD License, which is listed below

  This license applies to the TurboJPEG API library and associated programs,
  [libspng](https://libspng.org) (which is used by cjpeg and djpeg), and the
  build/test system.

  * The TurboJPEG API library wraps the libjpeg API library, so in the context
    of the overall TurboJPEG API library, both the terms of the IJG License and
    the terms of the Modified (3-clause) BSD License apply.
  * cjpeg and djpeg use libspng, so in the context of those programs, both the
    terms of the IJG License and the terms of the Modified (3-clause) BSD
    License apply.


Component Licenses
==================

Some of libjpeg-turbo's modules and internal dependencies are covered by less
restrictive licenses, but in the context of libjpeg-turbo as a whole, the terms
of the less restrictive licenses are subsumed by either the IJG License or the
Modified BSD License.  (In other words, the terms of the less restrictive
licenses are satisfied if the terms of the IJG and Modified BSD Licenses are
satisfied.)

- The libjpeg-turbo SIMD source code and zlib are covered by the
  [zlib License](https://spdx.org/licenses/Zlib.html), which is subsumed by the
  IJG License in the context of the cjpeg and djpeg programs and the libjpeg
  API library.

- Some of the libspng source code is covered by the
  [PNG Reference Library License v2](https://spdx.org/licenses/libpng-2.0.html),
  which is subsumed by the IJG License in the context of the cjpeg and djpeg
  programs and the TurboJPEG API library.

- Most of the libspng source code is covered by the
  [Simplified (2-clause) BSD License](https://spdx.org/licenses/BSD-2-Clause.html),
  which is subsumed by the Modified BSD License in the context of the cjpeg and
  djpeg programs and the TurboJPEG API library.


Complying with the libjpeg-turbo Licenses
=========================================

This section provides a roll-up of the libjpeg-turbo licensing terms, to the
best of our understanding.  This is not a license in and of itself.  It is
intended solely for clarification.

1.  If you are distributing a modified version of the libjpeg-turbo source,
    then:

    1.  You cannot alter or remove any existing copyright or license notices
        from the source.

        **Origin**
        - Clause 1 of the IJG License
        - Clause 1 of the Modified BSD License

    2.  You must add your own copyright notice to the header of each source
        file you modified, so others can tell that you modified that file.  (If
        there is not an existing copyright header in that file, then you can
        simply add a notice stating that you modified the file.)

        **Origin**
        - Clause 1 of the IJG License

    3.  You must include the IJG README file, and you must not alter any of the
        copyright or license text in that file.

        **Origin**
        - Clause 1 of the IJG License

2.  If you are distributing only libjpeg-turbo binaries without the source, or
    if you are distributing an application that statically links with
    libjpeg-turbo, then:

    1.  Your product documentation must include a message stating:

        This software is based in part on the work of the Independent JPEG
        Group.

        **Origin**
        - Clause 2 of the IJG license

    2.  If your binary distribution includes or uses the TurboJPEG API or
        associated programs, cjpeg, or djpeg, then your product documentation
        must include the text of the Modified BSD License (see below.)

        **Origin**
        - Clause 2 of the Modified BSD License

3.  You cannot use the name of the IJG or The libjpeg-turbo Project or the
    contributors thereof in advertising, publicity, etc.

    **Origin**
    - IJG License
    - Clause 3 of the Modified BSD License

4.  The authors and distributors do not warrant libjpeg-turbo to be free of
    defects, nor do we accept any liability for undesirable consequences
    resulting from your use of the software.

    **Origin**
    - IJG License
    - Modified BSD License


The Modified (3-clause) BSD License
===================================

Copyright (C) 2009-2026 D. R. Commander<br>
Copyright (C) 2018-2023 Randy <randy408@protonmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the libjpeg-turbo Project nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS",
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libjpeg-turbo/README.ijg

```text
libjpeg-turbo note:  This file has been modified by The libjpeg-turbo Project
to include only information relevant to libjpeg-turbo, to wordsmith certain
sections, and to remove impolitic language that existed in the libjpeg v8
README.  It is included only for reference.  Please see README.md for
information specific to libjpeg-turbo.


The Independent JPEG Group's JPEG software
==========================================

This distribution contains a release of the Independent JPEG Group's free JPEG
software.  You are welcome to redistribute this software and to use it for any
purpose, subject to the conditions under LEGAL ISSUES, below.

This software is the work of Tom Lane, Guido Vollbeding, Philip Gladstone,
Bill Allombert, Jim Boucher, Lee Crocker, Bob Friesenhahn, Ben Jackson,
Julian Minguillon, Luis Ortiz, George Phillips, Davide Rossi, Ge' Weijers,
and other members of the Independent JPEG Group.

IJG is not affiliated with the ISO/IEC JTC1/SC29/WG1 standards committee
(also known as JPEG, together with ITU-T SG16).


DOCUMENTATION ROADMAP
=====================

This file contains the following sections:

OVERVIEW            General description of JPEG and the IJG software.
LEGAL ISSUES        Copyright, lack of warranty, terms of distribution.
REFERENCES          Where to learn more about JPEG.
ARCHIVE LOCATIONS   Where to find newer versions of this software.
FILE FORMAT WARS    Software *not* to get.
TO DO               Plans for future IJG releases.

Other documentation files in the distribution are:

User documentation:
  doc/usage.txt         Usage instructions for cjpeg, djpeg, jpegtran,
                        rdjpgcom, and wrjpgcom.
  doc/*.1               Unix-style man pages for programs (same info as
                        usage.txt).
  doc/wizard.txt        Advanced usage instructions for JPEG wizards only.
  doc/change.log        Version-to-version change highlights.
Programmer and internal documentation:
  doc/libjpeg.txt       How to use the JPEG library in your own programs.
  src/example.c         Sample code for calling the JPEG library.
  doc/structure.txt     Overview of the JPEG library's internal structure.
  doc/coderules.txt     Coding style rules --- please read if you contribute
                        code.

Please read at least usage.txt.  Some information can also be found in the JPEG
FAQ (Frequently Asked Questions) article.  See ARCHIVE LOCATIONS below to find
out where to obtain the FAQ article.

If you want to understand how the JPEG code works, we suggest reading one or
more of the REFERENCES, then looking at the documentation files (in roughly
the order listed) before diving into the code.


OVERVIEW
========

This package contains C software to implement JPEG image encoding, decoding,
and transcoding.  JPEG (pronounced "jay-peg") is a standardized compression
method for full-color and grayscale images.  JPEG's strong suit is compressing
photographic images or other types of images that have smooth color and
brightness transitions between neighboring pixels.  Images with sharp lines or
other abrupt features may not compress well with JPEG, and a higher JPEG
quality may have to be used to avoid visible compression artifacts with such
images.

JPEG is normally lossy, meaning that the output pixels are not necessarily
identical to the input pixels.  However, on photographic content and other
"smooth" images, very good compression ratios can be obtained with no visible
compression artifacts, and extremely high compression ratios are possible if
you are willing to sacrifice image quality (by reducing the "quality" setting
in the compressor.)

This software implements JPEG baseline, extended-sequential, progressive, and
lossless compression processes.  Provision is made for supporting all variants
of these processes, although some uncommon parameter settings aren't
implemented yet.  We have made no provision for supporting the hierarchical
processes defined in the standard.

We provide a set of library routines for reading and writing JPEG image files,
plus two sample applications "cjpeg" and "djpeg", which use the library to
perform conversion between JPEG and some other popular image file formats.
The library is intended to be reused in other applications.

In order to support file conversion and viewing software, we have included
considerable functionality beyond the bare JPEG coding/decoding capability;
for example, the color quantization modules are not strictly part of JPEG
decoding, but they are essential for output to colormapped file formats.  These
extra functions can be compiled out of the library if not required for a
particular application.

We have also included "jpegtran", a utility for lossless transcoding between
different JPEG processes, and "rdjpgcom" and "wrjpgcom", two simple
applications for inserting and extracting textual comments in JFIF files.

The emphasis in designing this software has been on achieving portability and
flexibility, while also making it fast enough to be useful.  In particular,
the software is not intended to be read as a tutorial on JPEG.  (See the
REFERENCES section for introductory material.)  Rather, it is intended to
be reliable, portable, industrial-strength code.  We do not claim to have
achieved that goal in every aspect of the software, but we strive for it.

We welcome the use of this software as a component of commercial products.
No royalty is required, but we do ask for an acknowledgement in product
documentation, as described under LEGAL ISSUES.


LEGAL ISSUES
============

In plain English:

1. We don't promise that this software works.  (But if you find any bugs,
   please let us know!)
2. You can use this software for whatever you want.  You don't have to pay us.
3. You may not pretend that you wrote this software.  If you use it in a
   program, you must acknowledge somewhere in your documentation that
   you've used the IJG code.

In legalese:

The authors make NO WARRANTY or representation, either express or implied,
with respect to this software, its quality, accuracy, merchantability, or
fitness for a particular purpose.  This software is provided "AS IS", and you,
its user, assume the entire risk as to its quality and accuracy.

This software is copyright (C) 1991-2020, Thomas G. Lane, Guido Vollbeding.
All Rights Reserved except as specified below.

Permission is hereby granted to use, copy, modify, and distribute this
software (or portions thereof) for any purpose, without fee, subject to these
conditions:
(1) If any part of the source code for this software is distributed, then this
README file must be included, with this copyright and no-warranty notice
unaltered; and any additions, deletions, or changes to the original files
must be clearly indicated in accompanying documentation.
(2) If only executable code is distributed, then the accompanying
documentation must state that "this software is based in part on the work of
the Independent JPEG Group".
(3) Permission for use of this software is granted only if the user accepts
full responsibility for any undesirable consequences; the authors accept
NO LIABILITY for damages of any kind.

These conditions apply to any software derived from or based on the IJG code,
not just to the unmodified library.  If you use our work, you ought to
acknowledge us.

Permission is NOT granted for the use of any IJG author's name or company name
in advertising or publicity relating to this software or products derived from
it.  This software may be referred to only as "the Independent JPEG Group's
software".

We specifically permit and encourage the use of this software as the basis of
commercial products, provided that all warranty or liability claims are
assumed by the product vendor.


REFERENCES
==========

We recommend reading one or more of these references before trying to
understand the innards of the JPEG software.

The best short technical introduction to the JPEG compression algorithm is
        Wallace, Gregory K.  "The JPEG Still Picture Compression Standard",
        Communications of the ACM, April 1991 (vol. 34 no. 4), pp. 30-44.
(Adjacent articles in that issue discuss MPEG motion picture compression,
applications of JPEG, and related topics.)  If you don't have the CACM issue
handy, a PDF file containing a revised version of Wallace's article is
available at http://www.ijg.org/files/Wallace.JPEG.pdf.  The file (actually
a preprint for an article that appeared in IEEE Trans. Consumer Electronics)
omits the sample images that appeared in CACM, but it includes corrections
and some added material.  Note: the Wallace article is copyright ACM and IEEE,
and it may not be used for commercial purposes.

A somewhat less technical, more leisurely introduction to JPEG can be found in
"The Data Compression Book" by Mark Nelson and Jean-loup Gailly, published by
M&T Books (New York), 2nd ed. 1996, ISBN 1-55851-434-1.  This book provides
good explanations and example C code for a multitude of compression methods
including JPEG.  It is an excellent source if you are comfortable reading C
code but don't know much about data compression in general.  The book's JPEG
sample code is far from industrial-strength, but when you are ready to look
at a full implementation, you've got one here...

The best currently available description of JPEG is the textbook "JPEG Still
Image Data Compression Standard" by William B. Pennebaker and Joan L.
Mitchell, published by Van Nostrand Reinhold, 1993, ISBN 0-442-01272-1.
Price US$59.95, 638 pp.  The book includes the complete text of the ISO JPEG
standards (DIS 10918-1 and draft DIS 10918-2).

The original JPEG standard is divided into two parts, Part 1 being the actual
specification, while Part 2 covers compliance testing methods.  Part 1 is
titled "Digital Compression and Coding of Continuous-tone Still Images,
Part 1: Requirements and guidelines" and has document numbers ISO/IEC IS
10918-1, ITU-T T.81.  Part 2 is titled "Digital Compression and Coding of
Continuous-tone Still Images, Part 2: Compliance testing" and has document
numbers ISO/IEC IS 10918-2, ITU-T T.83.

The JPEG standard does not specify all details of an interchangeable file
format.  For the omitted details, we follow the "JFIF" conventions, revision
1.02.  JFIF version 1 has been adopted as ISO/IEC 10918-5 (05/2013) and
Recommendation ITU-T T.871 (05/2011): Information technology - Digital
compression and coding of continuous-tone still images: JPEG File Interchange
Format (JFIF).  It is available as a free download in PDF file format from
https://www.iso.org/standard/54989.html and http://www.itu.int/rec/T-REC-T.871.
A PDF file of the older JFIF 1.02 specification is available at
http://www.w3.org/Graphics/JPEG/jfif3.pdf.

The TIFF 6.0 file format specification can be obtained from
http://mirrors.ctan.org/graphics/tiff/TIFF6.ps.gz.  The JPEG incorporation
scheme found in the TIFF 6.0 spec of 3-June-92 has a number of serious
problems.  IJG does not recommend use of the TIFF 6.0 design (TIFF Compression
tag 6).  Instead, we recommend the JPEG design proposed by TIFF Technical Note
#2 (Compression tag 7).  Copies of this Note can be obtained from
http://www.ijg.org/files/.  It is expected that the next revision
of the TIFF spec will replace the 6.0 JPEG design with the Note's design.
Although IJG's own code does not support TIFF/JPEG, the free libtiff library
uses our library to implement TIFF/JPEG per the Note.


ARCHIVE LOCATIONS
=================

The "official" archive site for this software is www.ijg.org.
The most recent released version can always be found there in
directory "files".

The JPEG FAQ (Frequently Asked Questions) article is a source of some
general information about JPEG.  It is available at
http://www.faqs.org/faqs/jpeg-faq.


FILE FORMAT COMPATIBILITY
=========================

This software implements ITU T.81 | ISO/IEC 10918 with some extensions from
ITU T.871 | ISO/IEC 10918-5 (JPEG File Interchange Format-- see REFERENCES).
Informally, the term "JPEG image" or "JPEG file" most often refers to JFIF or
a subset thereof, but there are other formats containing the name "JPEG" that
are incompatible with the original JPEG standard or with JFIF (for instance,
JPEG 2000 and JPEG XR).  This software therefore does not support these
formats.  Indeed, one of the original reasons for developing this free software
was to help force convergence on a common, interoperable format standard for
JPEG files.

JFIF is a minimal or "low end" representation.  TIFF/JPEG (TIFF revision 6.0 as
modified by TIFF Technical Note #2) can be used for "high end" applications
that need to record a lot of additional data about an image.


TO DO
=====

Please send bug reports, offers of help, etc. to jpeg-info@jpegclub.org.
```

## liblzma (wheel copy) — 5.8.4

License: 0BSD

Upstream: https://github.com/tukaani-project/xz

### licenses/pillow-liblzma/COPYING

```text

XZ Utils Licensing
==================

    Different licenses apply to different files in this package. Here
    is a summary of which licenses apply to which parts of this package:

      - liblzma is under the BSD Zero Clause License (0BSD).

      - The command line tools xz, xzdec, lzmadec, and lzmainfo are
        under 0BSD except that, on systems that don't have a usable
        getopt_long, GNU getopt_long is compiled and linked in from the
        'lib' directory. The getopt_long code is under GNU LGPLv2.1+.

      - The scripts to grep, diff, and view compressed files have been
        adapted from GNU gzip. These scripts (xzgrep, xzdiff, xzless,
        and xzmore) are under GNU GPLv2+. The man pages of the scripts
        are under 0BSD; they aren't based on the man pages of GNU gzip.

      - Most of the XZ Utils specific documentation that is in
        plain text files (like README, INSTALL, PACKAGERS, NEWS,
        and ChangeLog) are under 0BSD unless stated otherwise in
        the file itself. The files xz-file-format.txt and
        lzma-file-format.xt are in the public domain but may
        be distributed under the terms of 0BSD too.

      - Translated messages and man pages are under 0BSD except that
        some old translations are in the public domain.

      - Test files and test code in the 'tests' directory, and
        debugging utilities in the 'debug' directory are under
        the BSD Zero Clause License (0BSD).

      - The GNU Autotools based build system contains files that are
        under GNU GPLv2+, GNU GPLv3+, and a few permissive licenses.
        These files don't affect the licensing of the binaries being
        built.

      - The 'extra' directory contains files that are under various
        free software licenses. These aren't built or installed as
        part of XZ Utils.

    The following command may be helpful in finding per-file license
    information. It works on xz.git and on a clean file tree extracted
    from a release tarball.

        sh build-aux/license-check.sh -v

    For the files under the BSD Zero Clause License (0BSD), if
    a copyright notice is needed, the following is sufficient:

        Copyright (C) The XZ Utils authors and contributors

    If you copy significant amounts of 0BSD-licensed code from XZ Utils
    into your project, acknowledging this somewhere in your software is
    polite (especially if it is proprietary, non-free software), but
    it is not legally required by the license terms. Here is an example
    of a good notice to put into "about box" or into documentation:

        This software includes code from XZ Utils <https://tukaani.org/xz/>.

    The following license texts are included in the following files:
      - COPYING.0BSD: BSD Zero Clause License
      - COPYING.LGPLv2.1: GNU Lesser General Public License version 2.1
      - COPYING.GPLv2: GNU General Public License version 2
      - COPYING.GPLv3: GNU General Public License version 3

    If you have questions, don't hesitate to ask for more information.
    The contact information is in the README file.
```

### licenses/pillow-liblzma/COPYING.0BSD

```text
Permission to use, copy, modify, and/or distribute this
software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## libtiff — 4.7.2

License: libtiff

Upstream: https://libtiff.gitlab.io/

### licenses/pillow-libtiff/LICENSE.md

```text
# LibTIFF license

Copyright © 1988-1997 Sam Leffler\
Copyright © 1991-1997 Silicon Graphics, Inc.

Permission to use, copy, modify, distribute, and sell this software and 
its documentation for any purpose is hereby granted without fee, provided
that (i) the above copyright notices and this permission notice appear in
all copies of the software and related documentation, and (ii) the names of
Sam Leffler and Silicon Graphics may not be used in any advertising or
publicity relating to the software without the specific, prior written
permission of Sam Leffler and Silicon Graphics.

THE SOFTWARE IS PROVIDED "AS-IS" AND WITHOUT WARRANTY OF ANY KIND, 
EXPRESS, IMPLIED OR OTHERWISE, INCLUDING WITHOUT LIMITATION, ANY 
WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  

IN NO EVENT SHALL SAM LEFFLER OR SILICON GRAPHICS BE LIABLE FOR
ANY SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY KIND,
OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER OR NOT ADVISED OF THE POSSIBILITY OF DAMAGE, AND ON ANY THEORY OF 
LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE 
OF THIS SOFTWARE.

# Lempel-Ziv & Welch Compression (tif_lzw.c) license
The code of tif_lzw.c is derived from the compress program whose code is
derived from software contributed to Berkeley by James A. Woods,
derived from original work by Spencer Thomas and Joseph Orost.

The original Berkeley copyright notice appears below in its entirety:

Copyright (c) 1985, 1986 The Regents of the University of California.
All rights reserved.

This code is derived from software contributed to Berkeley by
James A. Woods, derived from original work by Spencer Thomas
and Joseph Orost.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the University of California, Berkeley.  The name of the
University may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.
```

## libwebp, libwebpdemux, libwebpmux, libsharpyuv — 1.6.0

License: BSD-3-Clause + patent grant

Upstream: https://chromium.googlesource.com/webm/libwebp/

### licenses/pillow-libwebp/COPYING

```text
Copyright (c) 2010, Google Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libwebp/PATENTS

```text
Additional IP Rights Grant (Patents)
------------------------------------

"These implementations" means the copyrightable works that implement the WebM
codecs distributed by Google as part of the WebM Project.

Google hereby grants to you a perpetual, worldwide, non-exclusive, no-charge,
royalty-free, irrevocable (except as stated in this section) patent license to
make, have made, use, offer to sell, sell, import, transfer, and otherwise
run, modify and propagate the contents of these implementations of WebM, where
such license applies only to those patent claims, both currently owned by
Google and acquired in the future, licensable by Google that are necessarily
infringed by these implementations of WebM. This grant does not include claims
that would be infringed only as a consequence of further modification of these
implementations. If you or your agent or exclusive licensee institute or order
or agree to the institution of patent litigation or any other patent
enforcement activity against any entity (including a cross-claim or
counterclaim in a lawsuit) alleging that any of these implementations of WebM
or any code incorporated within any of these implementations of WebM
constitute direct or contributory patent infringement, or inducement of
patent infringement, then any patent rights granted to you under this License
for these implementations of WebM shall terminate as of the date such
litigation is filed.
```

### licenses/pillow-libwebp/AUTHORS

```text
Contributors:
- Aidan O'Loan (aidanol at gmail dot com)
- Alan Browning (browning at google dot com)
- Alexandru Ardelean (ardeleanalex at gmail dot com)
- Anuraag Agrawal (anuraaga at gmail dot com)
- Arthur Eubanks (aeubanks at google dot com)
- Brian Ledger (brianpl at google dot com)
- Charles Munger (clm at google dot com)
- Cheng Yi (cyi at google dot com)
- Christian Duvivier (cduvivier at google dot com)
- Christopher Degawa (ccom at randomderp dot com)
- Clement Courbet (courbet at google dot com)
- devtools-clrobot at google dot com (devtools-clrobot@google dot com)
- Djordje Pesut (djordje dot pesut at imgtec dot com)
- Frank (1433351828 at qq dot com)
- Frank Barchard (fbarchard at google dot com)
- Henner Zeller (hzeller at google dot com)
- Hui Su (huisu at google dot com)
- H. Vetinari (h dot vetinari at gmx dot com)
- Ilya Kurdyukov (jpegqs at gmail dot com)
- Ingvar Stepanyan (rreverser at google dot com)
- Istvan Stefan (Istvan dot Stefan at arm dot com)
- James Zern (jzern at google dot com)
- Jan Engelhardt (jengelh at medozas dot de)
- Jehan (jehan at girinstud dot io)
- Jeremy Maitin-Shepard (jbms at google dot com)
- Johann Koenig (johann dot koenig at duck dot com)
- Jonathan Grant (jgrantinfotech at gmail dot com)
- Jonliu1993 (13720414433 at 163 dot com)
- Jovan Zelincevic (jovan dot zelincevic at imgtec dot com)
- Jyrki Alakuijala (jyrki at google dot com)
- Konstantin Ivlev (tomskside at gmail dot com)
- Lode Vandevenne (lode at google dot com)
- Lou Quillio (louquillio at google dot com)
- Mans Rullgard (mans at mansr dot com)
- Marcin Kowalczyk (qrczak at google dot com)
- Martin Olsson (mnemo at minimum dot se)
- Maryla Ustarroz-Calonge (maryla at google dot com)
- Masahiro Hanada (hanada at atmark-techno dot com)
- Mikołaj Zalewski (mikolajz at google dot com)
- Mislav Bradac (mislavm at google dot com)
- natewood (natewood at fb dot com)
- Nico Weber (thakis at chromium dot org)
- Noel Chromium (noel at chromium dot org)
- Nozomi Isozaki (nontan at pixiv dot co dot jp)
- Oliver Wolff (oliver dot wolff at qt dot io)
- Owen Rodley (orodley at google dot com)
- Ozkan Sezer (sezeroz at gmail dot com)
- Parag Salasakar (img dot mips1 at gmail dot com)
- Pascal Massimino (pascal dot massimino at gmail dot com)
- Paweł Hajdan, Jr (phajdan dot jr at chromium dot org)
- Pierre Joye (pierre dot php at gmail dot com)
- Roberto Alanis (alanisbaez at google dot com)
- Sam Clegg (sbc at chromium dot org)
- Scott Hancher (seh at google dot com)
- Scott LaVarnway (slavarnway at google dot com)
- Scott Talbot (s at chikachow dot org)
- Slobodan Prijic (slobodan dot prijic at imgtec dot com)
- Somnath Banerjee (somnath dot banerjee at gmail dot com)
- Sriraman Tallam (tmsriram at google dot com)
- Tamar Levy (tamar dot levy at intel dot com)
- Thiago Perrotta (tperrotta at google dot com)
- Timothy Gu (timothygu99 at gmail dot com)
- Urvang Joshi (urvang at google dot com)
- Vikas Arora (vikasa at google dot com)
- Vincent Rabaud (vrabaud at google dot com)
- Vlad Tsyrklevich (vtsyrklevich at chromium dot org)
- Wan-Teh Chang (wtc at google dot com)
- wrv (wrv at utexas dot edu)
- Yang Zhang (yang dot zhang at arm dot com)
- Yannis Guyon (yguyon at google dot com)
- Zhi An Ng (zhin at chromium dot org)
```

## libxcb — 1.17.0

License: X11/MIT-style

Upstream: https://xcb.freedesktop.org/dist/libxcb-1.17.0.tar.xz

### licenses/pillow-libxcb/COPYING

```text
Copyright (C) 2001-2006 Bart Massey, Jamey Sharp, and Josh Triplett.
All Rights Reserved.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the names of the authors
or their institutions shall not be used in advertising or
otherwise to promote the sale, use or other dealings in this
Software without prior written authorization from the
authors.
```

## libyuv — 1924 (644251f252a84bf8ce91ff0aca86a9b16b069ab8)

License: BSD-3-Clause + patent grant

Upstream: https://chromium.googlesource.com/libyuv/libyuv/

### licenses/pillow-libyuv/LICENSE

```text
Copyright 2011 The LibYuv Project Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/pillow-libyuv/AUTHORS

```text
# Names should be added to this file like so:
# Name or Organization <email address>

Google Inc.

Ho Cheung <uioptt24@gmail.com>
Ivan Pavlotskiy <ivan.pavlotskiy@lgepartner.com>
```

### licenses/pillow-libyuv/PATENTS

```text
Additional IP Rights Grant (Patents)

"This implementation" means the copyrightable works distributed by
Google as part of the LibYuv code package.

Google hereby grants to you a perpetual, worldwide, non-exclusive,
no-charge, irrevocable (except as stated in this section) patent
license to make, have made, use, offer to sell, sell, import,
transfer, and otherwise run, modify and propagate the contents of this
implementation of the LibYuv code package, where such license applies
only to those patent claims, both currently owned by Google and
acquired in the future, licensable by Google that are necessarily
infringed by this implementation of the LibYuv code package. This
grant does not include claims that would be infringed only as a
consequence of further modification of this implementation. If you or
your agent or exclusive licensee institute or order or agree to the
institution of patent litigation against any entity (including a
cross-claim or counterclaim in a lawsuit) alleging that this
implementation of the LibYuv code package or any code incorporated
within this implementation of the LibYuv code package constitutes
direct or contributory patent infringement, or inducement of patent
infringement, then any patent rights granted to you under this License
for this implementation of the LibYuv code package shall terminate as
of the date such litigation is filed.
```

## OpenJPEG — 2.5.4

License: BSD-2-Clause

Upstream: https://github.com/uclouvain/openjpeg

### licenses/pillow-openjpeg/LICENSE

```text
/*
 * The copyright in this software is being made available under the 2-clauses 
 * BSD License, included below. This software may be subject to other third 
 * party and contributor rights, including patent rights, and no such rights
 * are granted under this license.
 *
 * Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium
 * Copyright (c) 2002-2014, Professor Benoit Macq
 * Copyright (c) 2003-2014, Antonin Descampe
 * Copyright (c) 2003-2009, Francois-Olivier Devaux
 * Copyright (c) 2005, Herve Drolon, FreeImage Team
 * Copyright (c) 2002-2003, Yannick Verschueren
 * Copyright (c) 2001-2003, David Janssens
 * Copyright (c) 2011-2012, Centre National d'Etudes Spatiales (CNES), France 
 * Copyright (c) 2012, CS Systemes d'Information, France
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS `AS IS'
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
```

## pythoncapi-compat (Pillow helper header) — b4cf22061a629428ceb19927f903732b8c20ef87 (Pillow 13.0.0)

License: 0BSD

Upstream: https://github.com/python/pythoncapi-compat

### licenses/pillow-pythoncapi-compat/COPYING

```text
BSD Zero Clause License

Copyright Contributors to the pythoncapi_compat project.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```

## Zstandard (wheel copy) — 1.5.7

License: BSD-3-Clause (selected alternative)

Upstream: https://github.com/facebook/zstd

### licenses/pillow-zstd/LICENSE

```text
BSD License

For Zstandard software

Copyright (c) Meta Platforms, Inc. and affiliates. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

 * Neither the name Facebook, nor Meta, nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## charset-normalizer — 3.5.2

License: MIT

Upstream: https://github.com/jawah/charset_normalizer/blob/3.5.2/LICENSE

### licenses/python-charset-normalizer/LICENSE

```text
MIT License

Copyright (c) 2025 TAHRI Ahmed R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## pillow — 13.0.0

License: MIT-CMU

Upstream: https://pypi.org/project/pillow/13.0.0/#files

### licenses/python-pillow/LICENSE

```text
The Python Imaging Library (PIL) is

    Copyright © 1997-2011 by Secret Labs AB
    Copyright © 1995-2011 by Fredrik Lundh and contributors

Pillow is the friendly PIL fork. It is

    Copyright © 2010 by Jeffrey 'Alex' Clark and contributors

Like PIL, Pillow is licensed under the open source MIT-CMU License:

By obtaining, using, and/or copying this software and/or its associated
documentation, you agree that you have read, understood, and will comply
with the following terms and conditions:

Permission to use, copy, modify and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appears in all copies, and that
both that copyright notice and this permission notice appear in supporting
documentation, and that the name of Secret Labs AB or the author not be
used in advertising or publicity pertaining to distribution of the software
without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.


----

AOM

Copyright (c) 2016, Alliance for Open Media. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.


----

BROTLI

Copyright (c) 2009, 2010, 2013-2016 by the Brotli Authors.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


----

BZIP2


--------------------------------------------------------------------------

This program, "bzip2", the associated library "libbzip2", and all
documentation, are copyright (C) 1996-2019 Julian R Seward.  All
rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. The origin of this software must not be misrepresented; you must
   not claim that you wrote the original software.  If you use this
   software in a product, an acknowledgment in the product
   documentation would be appreciated but is not required.

3. Altered source versions must be plainly marked as such, and must
   not be misrepresented as being the original software.

4. The name of the author may not be used to endorse or promote
   products derived from this software without specific prior written
   permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Julian Seward, jseward@acm.org
bzip2/libbzip2 version 1.0.8 of 13 July 2019

--------------------------------------------------------------------------


----

DAV1D

Copyright © 2018-2019, VideoLAN and dav1d authors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


----

FREETYPE2

The FreeType  2 font  engine is  copyrighted work  and cannot  be used
legally without  a software  license.  In order  to make  this project
usable to  a vast majority of  developers, we distribute it  under two
mutually exclusive open-source licenses.

This means that *you* must choose  *one* of the two licenses described
below, then obey all its terms and conditions when using FreeType 2 in
any of your projects or products.

  - The FreeType License,  found in the file  `docs/FTL.TXT`, which is
    similar to the  original BSD license *with*  an advertising clause
    that forces  you to explicitly  cite the FreeType project  in your
    product's  documentation.  All  details are  in the  license file.
    This license is suited to products which don't use the GNU General
    Public License.

    Note that  this license  is compatible to  the GNU  General Public
    License version 3, but not version 2.

  - The   GNU   General   Public   License   version   2,   found   in
    `docs/GPLv2.TXT`  (any  later  version  can  be  used  also),  for
    programs  which  already  use  the  GPL.  Note  that  the  FTL  is
    incompatible with GPLv2 due to its advertisement clause.

The contributed  BDF and PCF  drivers come  with a license  similar to
that  of the  X Window  System.   It is  compatible to  the above  two
licenses (see files `src/bdf/README`  and `src/pcf/README`).  The same
holds   for   the   source    code   files   `src/base/fthash.c`   and
`include/freetype/internal/fthash.h`; they were part of the BDF driver
in earlier FreeType versions.

The gzip  module uses the  zlib license (see  `src/gzip/zlib.h`) which
too is compatible to the above two licenses.

The files `src/autofit/ft-hb.c` and `src/autofit/ft-hb.h` contain code
taken almost  verbatim from the  HarfBuzz file `hb-ft.cc`,  which uses
the 'Old MIT' license, compatible to the above two licenses.

The  MD5 checksum  support  (only used  for  debugging in  development
builds) is in the public domain.

--------------------------------------------------------------------------

                    The FreeType Project LICENSE
                    ----------------------------

                            2006-Jan-27

                    Copyright 1996-2002, 2006 by
          David Turner, Robert Wilhelm, and Werner Lemberg



Introduction
============

  The FreeType  Project is distributed in  several archive packages;
  some of them may contain, in addition to the FreeType font engine,
  various tools and  contributions which rely on, or  relate to, the
  FreeType Project.

  This  license applies  to all  files found  in such  packages, and
  which do not  fall under their own explicit  license.  The license
  affects  thus  the  FreeType   font  engine,  the  test  programs,
  documentation and makefiles, at the very least.

  This  license   was  inspired  by  the  BSD,   Artistic,  and  IJG
  (Independent JPEG  Group) licenses, which  all encourage inclusion
  and  use of  free  software in  commercial  and freeware  products
  alike.  As a consequence, its main points are that:

    o We don't promise that this software works. However, we will be
      interested in any kind of bug reports. (`as is' distribution)

    o You can  use this software for whatever you  want, in parts or
      full form, without having to pay us. (`royalty-free' usage)

    o You may not pretend that  you wrote this software.  If you use
      it, or  only parts of it,  in a program,  you must acknowledge
      somewhere  in  your  documentation  that  you  have  used  the
      FreeType code. (`credits')

  We  specifically  permit  and  encourage  the  inclusion  of  this
  software, with  or without modifications,  in commercial products.
  We  disclaim  all warranties  covering  The  FreeType Project  and
  assume no liability related to The FreeType Project.


  Finally,  many  people  asked  us  for  a  preferred  form  for  a
  credit/disclaimer to use in compliance with this license.  We thus
  encourage you to use the following text:

   """
    Portions of this software are copyright © <year> The FreeType
    Project (www.freetype.org).  All rights reserved.
   """

  Please replace <year> with the value from the FreeType version you
  actually use.


Legal Terms
===========

0. Definitions
--------------

  Throughout this license,  the terms `package', `FreeType Project',
  and  `FreeType  archive' refer  to  the  set  of files  originally
  distributed  by the  authors  (David Turner,  Robert Wilhelm,  and
  Werner Lemberg) as the `FreeType Project', be they named as alpha,
  beta or final release.

  `You' refers to  the licensee, or person using  the project, where
  `using' is a generic term including compiling the project's source
  code as  well as linking it  to form a  `program' or `executable'.
  This  program is  referred to  as  `a program  using the  FreeType
  engine'.

  This  license applies  to all  files distributed  in  the original
  FreeType  Project,   including  all  source   code,  binaries  and
  documentation,  unless  otherwise  stated   in  the  file  in  its
  original, unmodified form as  distributed in the original archive.
  If you are  unsure whether or not a particular  file is covered by
  this license, you must contact us to verify this.

  The FreeType  Project is copyright (C) 1996-2000  by David Turner,
  Robert Wilhelm, and Werner Lemberg.  All rights reserved except as
  specified below.

1. No Warranty
--------------

  THE FREETYPE PROJECT  IS PROVIDED `AS IS' WITHOUT  WARRANTY OF ANY
  KIND, EITHER  EXPRESS OR IMPLIED,  INCLUDING, BUT NOT  LIMITED TO,
  WARRANTIES  OF  MERCHANTABILITY   AND  FITNESS  FOR  A  PARTICULAR
  PURPOSE.  IN NO EVENT WILL ANY OF THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE  FOR ANY DAMAGES CAUSED  BY THE USE OR  THE INABILITY TO
  USE, OF THE FREETYPE PROJECT.

2. Redistribution
-----------------

  This  license  grants  a  worldwide, royalty-free,  perpetual  and
  irrevocable right  and license to use,  execute, perform, compile,
  display,  copy,   create  derivative  works   of,  distribute  and
  sublicense the  FreeType Project (in  both source and  object code
  forms)  and  derivative works  thereof  for  any  purpose; and  to
  authorize others  to exercise  some or all  of the  rights granted
  herein, subject to the following conditions:

    o Redistribution of  source code  must retain this  license file
      (`FTL.TXT') unaltered; any  additions, deletions or changes to
      the original  files must be clearly  indicated in accompanying
      documentation.   The  copyright   notices  of  the  unaltered,
      original  files must  be  preserved in  all  copies of  source
      files.

    o Redistribution in binary form must provide a  disclaimer  that
      states  that  the software is based in part of the work of the
      FreeType Team,  in  the  distribution  documentation.  We also
      encourage you to put an URL to the FreeType web page  in  your
      documentation, though this isn't mandatory.

  These conditions  apply to any  software derived from or  based on
  the FreeType Project,  not just the unmodified files.   If you use
  our work, you  must acknowledge us.  However, no  fee need be paid
  to us.

3. Advertising
--------------

  Neither the  FreeType authors and  contributors nor you  shall use
  the name of the  other for commercial, advertising, or promotional
  purposes without specific prior written permission.

  We suggest,  but do not require, that  you use one or  more of the
  following phrases to refer  to this software in your documentation
  or advertising  materials: `FreeType Project',  `FreeType Engine',
  `FreeType library', or `FreeType Distribution'.

  As  you have  not signed  this license,  you are  not  required to
  accept  it.   However,  as  the FreeType  Project  is  copyrighted
  material, only  this license, or  another one contracted  with the
  authors, grants you  the right to use, distribute,  and modify it.
  Therefore,  by  using,  distributing,  or modifying  the  FreeType
  Project, you indicate that you understand and accept all the terms
  of this license.

4. Contacts
-----------

  There are two mailing lists related to FreeType:

    o freetype@nongnu.org

      Discusses general use and applications of FreeType, as well as
      future and  wanted additions to the  library and distribution.
      If  you are looking  for support,  start in  this list  if you
      haven't found anything to help you in the documentation.

    o freetype-devel@nongnu.org

      Discusses bugs,  as well  as engine internals,  design issues,
      specific licenses, porting, etc.

  Our home page can be found at

    https://www.freetype.org


--- end of FTL.TXT ---

The following license details are part of `src/bdf/README`:

```
License
*******

Copyright (C) 2001-2002 by Francesco Zappa Nardelli

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*** Portions of the driver (that is, bdflib.c and bdf.h):

Copyright 2000 Computing Research Labs, New Mexico State University
Copyright 2001-2002, 2011 Francesco Zappa Nardelli

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE COMPUTING RESEARCH LAB OR NEW MEXICO STATE UNIVERSITY BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Credits
*******

This driver is based on excellent Mark Leisher's bdf library.  If you
find something good in this driver you should probably thank him, not
me.
```

The following license details are part of `src/pcf/README`:

```
License
*******

Copyright (C) 2000 by Francesco Zappa Nardelli

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Credits
*******

Keith Packard wrote the pcf driver found in XFree86.  His work is at
the same time the specification and the sample implementation of the
PCF format.  Undoubtedly, this driver is inspired from his work.
```


----

HARFBUZZ

HarfBuzz is licensed under the so-called "Old MIT" license.  Details follow.
For parts of HarfBuzz that are licensed under different licenses see individual
files names COPYING in subdirectories where applicable.

Copyright © 2010-2022  Google, Inc.
Copyright © 2015-2020  Ebrahim Byagowi
Copyright © 2019,2020  Facebook, Inc.
Copyright © 2012,2015  Mozilla Foundation
Copyright © 2011  Codethink Limited
Copyright © 2008,2010  Nokia Corporation and/or its subsidiary(-ies)
Copyright © 2009  Keith Stribley
Copyright © 2011  Martin Hosken and SIL International
Copyright © 2007  Chris Wilson
Copyright © 2005,2006,2020,2021,2022,2023  Behdad Esfahbod
Copyright © 2004,2007,2008,2009,2010,2013,2021,2022,2023  Red Hat, Inc.
Copyright © 1998-2005  David Turner and Werner Lemberg
Copyright © 2016  Igalia S.L.
Copyright © 2022  Matthias Clasen
Copyright © 2018,2021  Khaled Hosny
Copyright © 2018,2019,2020  Adobe, Inc
Copyright © 2013-2015  Alexei Podtelezhnikov

For full copyright notices consult the individual files in the package.


Permission is hereby granted, without written agreement and without
license or royalty fees, to use, copy, modify, and distribute this
software and its documentation for any purpose, provided that the
above copyright notice and the following two paragraphs appear in
all copies of this software.

IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE TO ANY PARTY FOR
DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN
IF THE COPYRIGHT HOLDER HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE COPYRIGHT HOLDER SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
ON AN "AS IS" BASIS, AND THE COPYRIGHT HOLDER HAS NO OBLIGATION TO
PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.


----

LCMS2

Little CMS
Copyright (c) 1998-2020 Marti Maria Saguer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


----

LIBAVIF

Copyright 2019 Joe Drago. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------------

Files: src/obu.c

Copyright © 2018-2019, VideoLAN and dav1d authors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------------

Files: third_party/iccjpeg/*

In plain English:

1. We don't promise that this software works.  (But if you find any bugs,
   please let us know!)
2. You can use this software for whatever you want.  You don't have to pay us.
3. You may not pretend that you wrote this software.  If you use it in a
   program, you must acknowledge somewhere in your documentation that
   you've used the IJG code.

In legalese:

The authors make NO WARRANTY or representation, either express or implied,
with respect to this software, its quality, accuracy, merchantability, or
fitness for a particular purpose.  This software is provided "AS IS", and you,
its user, assume the entire risk as to its quality and accuracy.

This software is copyright (C) 1991-2013, Thomas G. Lane, Guido Vollbeding.
All Rights Reserved except as specified below.

Permission is hereby granted to use, copy, modify, and distribute this
software (or portions thereof) for any purpose, without fee, subject to these
conditions:
(1) If any part of the source code for this software is distributed, then this
README file must be included, with this copyright and no-warranty notice
unaltered; and any additions, deletions, or changes to the original files
must be clearly indicated in accompanying documentation.
(2) If only executable code is distributed, then the accompanying
documentation must state that "this software is based in part on the work of
the Independent JPEG Group".
(3) Permission for use of this software is granted only if the user accepts
full responsibility for any undesirable consequences; the authors accept
NO LIABILITY for damages of any kind.

These conditions apply to any software derived from or based on the IJG code,
not just to the unmodified library.  If you use our work, you ought to
acknowledge us.

Permission is NOT granted for the use of any IJG author's name or company name
in advertising or publicity relating to this software or products derived from
it.  This software may be referred to only as "the Independent JPEG Group's
software".

We specifically permit and encourage the use of this software as the basis of
commercial products, provided that all warranty or liability claims are
assumed by the product vendor.


The Unix configuration script "configure" was produced with GNU Autoconf.
It is copyright by the Free Software Foundation but is freely distributable.
The same holds for its supporting scripts (config.guess, config.sub,
ltmain.sh).  Another support script, install-sh, is copyright by X Consortium
but is also freely distributable.

The IJG distribution formerly included code to read and write GIF files.
To avoid entanglement with the Unisys LZW patent, GIF reading support has
been removed altogether, and the GIF writer has been simplified to produce
"uncompressed GIFs".  This technique does not use the LZW algorithm; the
resulting GIF files are larger than usual, but are readable by all standard
GIF decoders.

We are required to state that
    "The Graphics Interchange Format(c) is the Copyright property of
    CompuServe Incorporated.  GIF(sm) is a Service Mark property of
    CompuServe Incorporated."

------------------------------------------------------------------------------

Files: contrib/gdk-pixbuf/*

Copyright 2020 Emmanuel Gil Peyrot. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------------

Files: android_jni/gradlew*


                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

------------------------------------------------------------------------------

Files: third_party/libyuv/*

Copyright 2011 The LibYuv Project Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


----

LIBJPEG

1. We don't promise that this software works.  (But if you find any bugs,
   please let us know!)
2. You can use this software for whatever you want.  You don't have to pay us.
3. You may not pretend that you wrote this software.  If you use it in a
   program, you must acknowledge somewhere in your documentation that
   you've used the IJG code.

In legalese:

The authors make NO WARRANTY or representation, either express or implied,
with respect to this software, its quality, accuracy, merchantability, or
fitness for a particular purpose.  This software is provided "AS IS", and you,
its user, assume the entire risk as to its quality and accuracy.

This software is copyright (C) 1991-2020, Thomas G. Lane, Guido Vollbeding.
All Rights Reserved except as specified below.

Permission is hereby granted to use, copy, modify, and distribute this
software (or portions thereof) for any purpose, without fee, subject to these
conditions:
(1) If any part of the source code for this software is distributed, then this
README file must be included, with this copyright and no-warranty notice
unaltered; and any additions, deletions, or changes to the original files
must be clearly indicated in accompanying documentation.
(2) If only executable code is distributed, then the accompanying
documentation must state that "this software is based in part on the work of
the Independent JPEG Group".
(3) Permission for use of this software is granted only if the user accepts
full responsibility for any undesirable consequences; the authors accept
NO LIABILITY for damages of any kind.

These conditions apply to any software derived from or based on the IJG code,
not just to the unmodified library.  If you use our work, you ought to
acknowledge us.

Permission is NOT granted for the use of any IJG author's name or company name
in advertising or publicity relating to this software or products derived from
it.  This software may be referred to only as "the Independent JPEG Group's
software".

We specifically permit and encourage the use of this software as the basis of
commercial products, provided that all warranty or liability claims are
assumed by the product vendor.


----

LIBLZMA

XZ Utils Licensing
==================

    Different licenses apply to different files in this package. Here
    is a rough summary of which licenses apply to which parts of this
    package (but check the individual files to be sure!):

      - liblzma is in the public domain.

      - xz, xzdec, and lzmadec command line tools are in the public
        domain unless GNU getopt_long had to be compiled and linked
        in from the lib directory. The getopt_long code is under
        GNU LGPLv2.1+.

      - The scripts to grep, diff, and view compressed files have been
        adapted from gzip. These scripts and their documentation are
        under GNU GPLv2+.

      - All the documentation in the doc directory and most of the
        XZ Utils specific documentation files in other directories
        are in the public domain.

      - Translated messages are in the public domain.

      - The build system contains public domain files, and files that
        are under GNU GPLv2+ or GNU GPLv3+. None of these files end up
        in the binaries being built.

      - Test files and test code in the tests directory, and debugging
        utilities in the debug directory are in the public domain.

      - The extra directory may contain public domain files, and files
        that are under various free software licenses.

    You can do whatever you want with the files that have been put into
    the public domain. If you find public domain legally problematic,
    take the previous sentence as a license grant. If you still find
    the lack of copyright legally problematic, you have too many
    lawyers.

    As usual, this software is provided "as is", without any warranty.

    If you copy significant amounts of public domain code from XZ Utils
    into your project, acknowledging this somewhere in your software is
    polite (especially if it is proprietary, non-free software), but
    naturally it is not legally required. Here is an example of a good
    notice to put into "about box" or into documentation:

        This software includes code from XZ Utils <http://tukaani.org/xz/>.

    The following license texts are included in the following files:
      - COPYING.LGPLv2.1: GNU Lesser General Public License version 2.1
      - COPYING.GPLv2: GNU General Public License version 2
      - COPYING.GPLv3: GNU General Public License version 3

    Note that the toolchain (compiler, linker etc.) may add some code
    pieces that are copyrighted. Thus, it is possible that e.g. liblzma
    binary wouldn't actually be in the public domain in its entirety
    even though it contains no copyrighted code from the XZ Utils source
    package.

    If you have questions, don't hesitate to ask the author(s) for more
    information.


----

LIBPNG

COPYRIGHT NOTICE, DISCLAIMER, and LICENSE
=========================================

PNG Reference Library License version 2
---------------------------------------

 * Copyright (c) 1995-2022 The PNG Reference Library Authors.
 * Copyright (c) 2018-2022 Cosmin Truta.
 * Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.
 * Copyright (c) 1996-1997 Andreas Dilger.
 * Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc.

The software is supplied "as is", without warranty of any kind,
express or implied, including, without limitation, the warranties
of merchantability, fitness for a particular purpose, title, and
non-infringement.  In no event shall the Copyright owners, or
anyone distributing the software, be liable for any damages or
other liability, whether in contract, tort or otherwise, arising
from, out of, or in connection with the software, or the use or
other dealings in the software, even if advised of the possibility
of such damage.

Permission is hereby granted to use, copy, modify, and distribute
this software, or portions hereof, for any purpose, without fee,
subject to the following restrictions:

 1. The origin of this software must not be misrepresented; you
    must not claim that you wrote the original software.  If you
    use this software in a product, an acknowledgment in the product
    documentation would be appreciated, but is not required.

 2. Altered source versions must be plainly marked as such, and must
    not be misrepresented as being the original software.

 3. This Copyright notice may not be removed or altered from any
    source or altered source distribution.


PNG Reference Library License version 1 (for libpng 0.5 through 1.6.35)
-----------------------------------------------------------------------

libpng versions 1.0.7, July 1, 2000, through 1.6.35, July 15, 2018 are
Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson, are
derived from libpng-1.0.6, and are distributed according to the same
disclaimer and license as libpng-1.0.6 with the following individuals
added to the list of Contributing Authors:

    Simon-Pierre Cadieux
    Eric S. Raymond
    Mans Rullgard
    Cosmin Truta
    Gilles Vollant
    James Yu
    Mandar Sahastrabuddhe
    Google Inc.
    Vadim Barkov

and with the following additions to the disclaimer:

    There is no warranty against interference with your enjoyment of
    the library or against infringement.  There is no warranty that our
    efforts or the library will fulfill any of your particular purposes
    or needs.  This library is provided with all faults, and the entire
    risk of satisfactory quality, performance, accuracy, and effort is
    with the user.

Some files in the "contrib" directory and some configure-generated
files that are distributed with libpng have other copyright owners, and
are released under other open source licenses.

libpng versions 0.97, January 1998, through 1.0.6, March 20, 2000, are
Copyright (c) 1998-2000 Glenn Randers-Pehrson, are derived from
libpng-0.96, and are distributed according to the same disclaimer and
license as libpng-0.96, with the following individuals added to the
list of Contributing Authors:

    Tom Lane
    Glenn Randers-Pehrson
    Willem van Schaik

libpng versions 0.89, June 1996, through 0.96, May 1997, are
Copyright (c) 1996-1997 Andreas Dilger, are derived from libpng-0.88,
and are distributed according to the same disclaimer and license as
libpng-0.88, with the following individuals added to the list of
Contributing Authors:

    John Bowler
    Kevin Bracey
    Sam Bushell
    Magnus Holmgren
    Greg Roelofs
    Tom Tanner

Some files in the "scripts" directory have other copyright owners,
but are released under this license.

libpng versions 0.5, May 1995, through 0.88, January 1996, are
Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc.

For the purposes of this copyright and license, "Contributing Authors"
is defined as the following set of individuals:

    Andreas Dilger
    Dave Martindale
    Guy Eric Schalnat
    Paul Schmidt
    Tim Wegner

The PNG Reference Library is supplied "AS IS".  The Contributing
Authors and Group 42, Inc. disclaim all warranties, expressed or
implied, including, without limitation, the warranties of
merchantability and of fitness for any purpose.  The Contributing
Authors and Group 42, Inc. assume no liability for direct, indirect,
incidental, special, exemplary, or consequential damages, which may
result from the use of the PNG Reference Library, even if advised of
the possibility of such damage.

Permission is hereby granted to use, copy, modify, and distribute this
source code, or portions hereof, for any purpose, without fee, subject
to the following restrictions:

 1. The origin of this source code must not be misrepresented.

 2. Altered versions must be plainly marked as such and must not
    be misrepresented as being the original source.

 3. This Copyright notice may not be removed or altered from any
    source or altered source distribution.

The Contributing Authors and Group 42, Inc. specifically permit,
without fee, and encourage the use of this source code as a component
to supporting the PNG file format in commercial products.  If you use
this source code in a product, acknowledgment is not required but would
be appreciated.


----

LIBTIFF

Copyright (c) 1988-1997 Sam Leffler
Copyright (c) 1991-1997 Silicon Graphics, Inc.

Permission to use, copy, modify, distribute, and sell this software and
its documentation for any purpose is hereby granted without fee, provided
that (i) the above copyright notices and this permission notice appear in
all copies of the software and related documentation, and (ii) the names of
Sam Leffler and Silicon Graphics may not be used in any advertising or
publicity relating to the software without the specific, prior written
permission of Sam Leffler and Silicon Graphics.

THE SOFTWARE IS PROVIDED "AS-IS" AND WITHOUT WARRANTY OF ANY KIND,
EXPRESS, IMPLIED OR OTHERWISE, INCLUDING WITHOUT LIMITATION, ANY
WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

IN NO EVENT SHALL SAM LEFFLER OR SILICON GRAPHICS BE LIABLE FOR
ANY SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY KIND,
OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER OR NOT ADVISED OF THE POSSIBILITY OF DAMAGE, AND ON ANY THEORY OF
LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.


----

LIBWEBP

Copyright (c) 2010, Google Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


----

LIBYUV

Copyright 2011 The LibYuv Project Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name of Google nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


----

OPENJPEG

*
 * The copyright in this software is being made available under the 2-clauses
 * BSD License, included below. This software may be subject to other third
 * party and contributor rights, including patent rights, and no such rights
 * are granted under this license.
 *
 * Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium
 * Copyright (c) 2002-2014, Professor Benoit Macq
 * Copyright (c) 2003-2014, Antonin Descampe
 * Copyright (c) 2003-2009, Francois-Olivier Devaux
 * Copyright (c) 2005, Herve Drolon, FreeImage Team
 * Copyright (c) 2002-2003, Yannick Verschueren
 * Copyright (c) 2001-2003, David Janssens
 * Copyright (c) 2011-2012, Centre National d'Etudes Spatiales (CNES), France
 * Copyright (c) 2012, CS Systemes d'Information, France
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS `AS IS'
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */


----

RAQM

The MIT License (MIT)

Copyright © 2015 Information Technology Authority (ITA) <foss@ita.gov.om>
Copyright © 2016 Khaled Hosny <khaledhosny@eglug.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


----

TCL_TK

This software is copyrighted by the Regents of the University
of California, Sun Microsystems, Inc., Scriptics Corporation,
and other parties. The following terms apply to all files
associated with the software unless explicitly disclaimed in
individual files.

The authors hereby grant permission to use, copy, modify,
distribute, and license this software and its documentation
for any purpose, provided that existing copyright notices are
retained in all copies and that this notice is included
verbatim in any distributions. No written agreement, license,
or royalty fee is required for any of the authorized uses.
Modifications to this software may be copyrighted by their
authors and need not follow the licensing terms described
here, provided that the new terms are clearly indicated on
the first page of each file where they apply.

IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO
ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR
CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS
SOFTWARE, ITS DOCUMENTATION, OR ANY DERIVATIVES THEREOF, EVEN
IF THE AUTHORS HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, AND NON-INFRINGEMENT. THIS SOFTWARE IS PROVIDED ON
AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE NO
OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.

GOVERNMENT USE: If you are acquiring this software on behalf
of the U.S. government, the Government shall have only
"Restricted Rights" in the software and related documentation
as defined in the Federal Acquisition Regulations (FARs) in
Clause 52.227.19 (c) (2). If you are acquiring the software
on behalf of the Department of Defense, the software shall be
classified as "Commercial Computer Software" and the
Government shall have only "Restricted Rights" as defined in
Clause 252.227-7013 (c) (1) of DFARs. Notwithstanding the
foregoing, the authors grant the U.S. Government and others
acting in its behalf permission to use and distribute the
software in accordance with the terms specified in this
license


----

XAU

Copyright 1988, 1993, 1994, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.


----

XCB

Copyright (C) 2001-2006 Bart Massey, Jamey Sharp, and Josh Triplett.
All Rights Reserved.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the names of the authors
or their institutions shall not be used in advertising or
otherwise to promote the sale, use or other dealings in this
Software without prior written authorization from the
authors.


----

XDMCP

Copyright 1989, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.

Author:  Keith Packard, MIT X Consortium


----

ZLIB

 (C) 1995-2017 Jean-loup Gailly and Mark Adler

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.

  Jean-loup Gailly        Mark Adler
  jloup@gzip.org          madler@alumni.caltech.edu

If you use the zlib library in a product, we would appreciate *not* receiving
lengthy legal documents to sign.  The sources are provided for free but without
warranty of any kind.  The library has been entirely written by Jean-loup
Gailly and Mark Adler; it does not include third-party code.

If you redistribute modified sources, we would appreciate that you include in
the file ChangeLog history information documenting your changes.  Please read
the FAQ for more information on the distribution of modified source versions.


----

ZSTD

BSD License

For Zstandard software

Copyright (c) Meta Platforms, Inc. and affiliates. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

 * Neither the name Facebook, nor Meta, nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### licenses/python-pillow/sboms/auditwheel.cdx.json

```text
{"bomFormat": "CycloneDX", "specVersion": "1.4", "version": 1, "metadata": {"component": {"type": "library", "bom-ref": "pkg:pypi/pillow@13.0.0?file_name=pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", "name": "pillow", "version": "13.0.0", "purl": "pkg:pypi/pillow@13.0.0?file_name=pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl"}, "tools": [{"name": "auditwheel", "version": "6.8.2"}]}, "components": [{"type": "library", "bom-ref": "pkg:pypi/pillow@13.0.0?file_name=pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", "name": "pillow", "version": "13.0.0", "purl": "pkg:pypi/pillow@13.0.0?file_name=pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl"}, {"type": "library", "bom-ref": "pkg:rpm/almalinux/libXau@1.0.9-3.el8#ac77887fa9a50833ff7a34d7e27ebe243468552bc94f6628693cb1dfdaf102e7", "name": "libXau", "version": "1.0.9-3.el8", "purl": "pkg:rpm/almalinux/libXau@1.0.9-3.el8"}], "dependencies": [{"ref": "pkg:pypi/pillow@13.0.0?file_name=pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", "dependsOn": ["pkg:rpm/almalinux/libXau@1.0.9-3.el8#ac77887fa9a50833ff7a34d7e27ebe243468552bc94f6628693cb1dfdaf102e7"]}, {"ref": "pkg:rpm/almalinux/libXau@1.0.9-3.el8#ac77887fa9a50833ff7a34d7e27ebe243468552bc94f6628693cb1dfdaf102e7"}]}
```

### licenses/python-pillow/sboms/pillow-13.0.0.cdx.json

```text
{
  "$schema": "http://cyclonedx.org/schema/bom-1.7.schema.json",
  "bomFormat": "CycloneDX",
  "specVersion": "1.7",
  "serialNumber": "urn:uuid:81a9dfa3-d713-4390-be28-45c6979b49ca",
  "version": 1,
  "metadata": {
    "timestamp": "2026-10-16T20:10:55Z",
    "lifecycles": [
      {
        "phase": "build"
      }
    ],
    "tools": {
      "components": [
        {
          "type": "application",
          "name": "generate-sbom.py",
          "group": "pillow"
        }
      ]
    },
    "component": {
      "bom-ref": "pkg:pypi/pillow@13.0.0",
      "type": "library",
      "name": "Pillow",
      "version": "13.0.0",
      "description": "Python Imaging Library (fork)",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0",
      "externalReferences": [
        {
          "type": "website",
          "url": "https://python-pillow.org"
        },
        {
          "type": "vcs",
          "url": "https://github.com/python-pillow/Pillow"
        },
        {
          "type": "documentation",
          "url": "https://pillow.readthedocs.io"
        },
        {
          "type": "security-contact",
          "url": "https://github.com/python-pillow/Pillow/security/policy"
        }
      ]
    }
  },
  "components": [
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._avif",
      "type": "library",
      "name": "PIL._avif",
      "version": "13.0.0",
      "description": "AVIF image format extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._avif"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imaging",
      "type": "library",
      "name": "PIL._imaging",
      "version": "13.0.0",
      "description": "Core image processing extension (decode, encode, map, display, outline, path, libImaging)",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imaging"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingcms",
      "type": "library",
      "name": "PIL._imagingcms",
      "version": "13.0.0",
      "description": "LittleCMS2 colour management extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingcms"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingft",
      "type": "library",
      "name": "PIL._imagingft",
      "version": "13.0.0",
      "description": "FreeType font rendering extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingft"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingmath",
      "type": "library",
      "name": "PIL._imagingmath",
      "version": "13.0.0",
      "description": "Image math operations extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingmath"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingmorph",
      "type": "library",
      "name": "PIL._imagingmorph",
      "version": "13.0.0",
      "description": "Image morphology extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingmorph"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingtk",
      "type": "library",
      "name": "PIL._imagingtk",
      "version": "13.0.0",
      "description": "Tk/Tcl display extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingtk"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._webp",
      "type": "library",
      "name": "PIL._webp",
      "version": "13.0.0",
      "description": "WebP image format extension",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "purl": "pkg:pypi/pillow@13.0.0#c-ext/PIL._webp"
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#thirdparty/fribidi-shim",
      "type": "library",
      "name": "fribidi-shim",
      "version": "1.x",
      "description": "FriBiDi runtime-loading shim (vendored in src/thirdparty/fribidi-shim/); loads libfribidi dynamically",
      "licenses": [
        {
          "license": {
            "id": "MIT-CMU"
          }
        }
      ],
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "1237c1af420466696635bcbcf5a7738b4662872dae7066df9df28c2e2f8603ea"
        }
      ],
      "pedigree": {
        "notes": "Pillow-authored shim; not taken from an upstream project. fribidi.h declares the subset of FriBiDi's public API types, constants and function signatures needed to load libfribidi at runtime. No FriBiDi implementation code is included."
      },
      "externalReferences": [
        {
          "type": "website",
          "url": "https://github.com/fribidi/fribidi"
        }
      ]
    },
    {
      "bom-ref": "pkg:github/python/pythoncapi-compat",
      "type": "library",
      "name": "pythoncapi_compat",
      "description": "Backport header for new CPython C-API functions (vendored in src/thirdparty/pythoncapi_compat.h)",
      "licenses": [
        {
          "license": {
            "id": "0BSD"
          }
        }
      ],
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "526f4e1a9f41c0dc641e24f723d85fe8b31b80405b6769510d998043907aa513"
        }
      ],
      "pedigree": {
        "notes": "Vendored unmodified from upstream python/pythoncapi-compat."
      },
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/python/pythoncapi-compat"
        }
      ]
    },
    {
      "bom-ref": "pkg:pypi/pillow@13.0.0#thirdparty/raqm",
      "type": "library",
      "name": "raqm",
      "version": "0.11.0",
      "description": "Complex text layout library (vendored in src/thirdparty/raqm/)",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "d3cb7309f91c5804fd19adc04efdcaf167d26e156f3459844b205b25dedca001"
        }
      ],
      "pedigree": {
        "ancestors": [
          {
            "bom-ref": "pkg:github/HOST-Oman/libraqm@0.11.0#upstream",
            "type": "library",
            "name": "raqm",
            "version": "0.11.0",
            "purl": "pkg:github/HOST-Oman/libraqm@0.11.0",
            "externalReferences": [
              {
                "type": "distribution",
                "url": "https://github.com/HOST-Oman/libraqm/releases/tag/v0.11.0"
              }
            ]
          }
        ],
        "patches": [
          {
            "type": "unofficial",
            "diff": {
              "text": {
                "content": "LS0tIGEvc3JjL3JhcW0tdmVyc2lvbi5oLmluCisrKyBiL3NyYy9yYXFtLXZlcnNpb24uaApAQCAtMzEsMTEgKzMxLDExIEBACiAjaWZuZGVmIF9SQVFNX1ZFUlNJT05fSF8KICNkZWZpbmUgX1JBUU1fVkVSU0lPTl9IXwogCi0jZGVmaW5lIFJBUU1fVkVSU0lPTl9NQUpPUiBAUkFRTV9WRVJTSU9OX01BSk9SQAotI2RlZmluZSBSQVFNX1ZFUlNJT05fTUlOT1IgQFJBUU1fVkVSU0lPTl9NSU5PUkAKLSNkZWZpbmUgUkFRTV9WRVJTSU9OX01JQ1JPIEBSQVFNX1ZFUlNJT05fTUlDUk9ACisjZGVmaW5lIFJBUU1fVkVSU0lPTl9NQUpPUiAwCisjZGVmaW5lIFJBUU1fVkVSU0lPTl9NSU5PUiAxMQorI2RlZmluZSBSQVFNX1ZFUlNJT05fTUlDUk8gMAogCi0jZGVmaW5lIFJBUU1fVkVSU0lPTl9TVFJJTkcgIkBSQVFNX1ZFUlNJT05AIgorI2RlZmluZSBSQVFNX1ZFUlNJT05fU1RSSU5HICIwLjExLjAiCiAKICNkZWZpbmUgUkFRTV9WRVJTSU9OX0FUTEVBU1QobWFqb3IsbWlub3IsbWljcm8pIFwKICAgICAgICAgKChtYWpvcikqMTAwMDArKG1pbm9yKSoxMDArKG1pY3JvKSA8PSBcCg==",
                "encoding": "base64"
              }
            }
          },
          {
            "type": "unofficial",
            "diff": {
              "text": {
                "content": "LS0tIGEvc3JjL3JhcW0uYworKysgYi9zcmMvcmFxbS5jCkBAIC0zNiw3ICszNiwxMSBAQAogI2luY2x1ZGUgPFNoZWVuQmlkaS5oPgogI2VuZGlmCiAjZWxzZQorI2lmZGVmIEhBVkVfRlJJQklESV9TWVNURU0KICNpbmNsdWRlIDxmcmliaWRpLmg+CisjZWxzZQorI2luY2x1ZGUgIi4uL2ZyaWJpZGktc2hpbS9mcmliaWRpLmgiCisjZW5kaWYKICNlbmRpZgogCiAjaW5jbHVkZSA8aGIuaD4K",
                "encoding": "base64"
              }
            }
          }
        ],
        "notes": "Vendored from upstream HOST-Oman/libraqm v0.11.0 with two Pillow-specific modifications: (1) raqm-version.h.in was pre-processed into raqm-version.h with version placeholders replaced by literal values; (2) raqm.c wraps the <fribidi.h> include in an #ifdef HAVE_FRIBIDI_SYSTEM guard so Pillow's bundled fribidi-shim is used when a system FriBiDi is absent."
      },
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/python-pillow/Pillow/tree/main/src/thirdparty/raqm"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/freetype2",
      "type": "library",
      "name": "FreeType",
      "version": "2.14.3",
      "scope": "optional",
      "description": "Font rendering (optional, used by PIL._imagingft). Required for text/font support.",
      "licenses": [
        {
          "license": {
            "id": "FTL"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://freetype.org"
        },
        {
          "type": "distribution",
          "url": "https://download.savannah.gnu.org/releases/freetype/"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/fribidi",
      "type": "library",
      "name": "FriBiDi",
      "version": "1.0.17",
      "scope": "optional",
      "description": "Unicode bidi algorithm library (optional, loaded at runtime by fribidi-shim).",
      "licenses": [
        {
          "license": {
            "id": "LGPL-2.1-or-later"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://github.com/fribidi/fribidi"
        },
        {
          "type": "distribution",
          "url": "https://github.com/fribidi/fribidi/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/harfbuzz",
      "type": "library",
      "name": "HarfBuzz",
      "version": "14.5.0",
      "scope": "optional",
      "description": "Text shaping (optional, required by libraqm for complex text layout).",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://harfbuzz.github.io"
        },
        {
          "type": "distribution",
          "url": "https://github.com/harfbuzz/harfbuzz/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/libavif",
      "type": "library",
      "name": "libavif",
      "version": "1.4.2",
      "scope": "optional",
      "description": "AVIF codec (optional, used by PIL._avif).",
      "licenses": [
        {
          "license": {
            "id": "BSD-2-Clause"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://github.com/AOMediaCodec/libavif"
        },
        {
          "type": "distribution",
          "url": "https://github.com/AOMediaCodec/libavif/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/libimagequant",
      "type": "library",
      "name": "libimagequant",
      "version": "4.4.1",
      "scope": "optional",
      "description": "Improved colour quantization (optional).",
      "licenses": [
        {
          "license": {
            "id": "GPL-3.0-or-later"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://pngquant.org/lib/"
        },
        {
          "type": "distribution",
          "url": "https://github.com/ImageOptim/libimagequant/tags"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/libjpeg",
      "type": "library",
      "name": "libjpeg / libjpeg-turbo",
      "version": "3.2.0",
      "description": "JPEG codec (required by default; disable with -C jpeg=disable).",
      "licenses": [
        {
          "license": {
            "id": "IJG"
          }
        },
        {
          "license": {
            "id": "BSD-3-Clause"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://ijg.org"
        },
        {
          "type": "website",
          "url": "https://libjpeg-turbo.org"
        },
        {
          "type": "distribution",
          "url": "https://github.com/libjpeg-turbo/libjpeg-turbo/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/libtiff",
      "type": "library",
      "name": "libtiff",
      "version": "4.7.2",
      "scope": "optional",
      "description": "TIFF codec (optional).",
      "licenses": [
        {
          "license": {
            "id": "libtiff"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://libtiff.gitlab.io/libtiff/"
        },
        {
          "type": "distribution",
          "url": "https://download.osgeo.org/libtiff/"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/libwebp",
      "type": "library",
      "name": "libwebp",
      "version": "1.6.0",
      "scope": "optional",
      "description": "WebP codec (optional, used by PIL._webp).",
      "licenses": [
        {
          "license": {
            "id": "BSD-3-Clause"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://chromium.googlesource.com/webm/libwebp"
        },
        {
          "type": "distribution",
          "url": "https://chromium.googlesource.com/webm/libwebp"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/libxcb",
      "type": "library",
      "name": "libxcb",
      "version": "1.17.0",
      "scope": "optional",
      "description": "X11 screen-grab support (optional, used by PIL._imaging on macOS and Linux).",
      "licenses": [
        {
          "license": {
            "id": "X11"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://xcb.freedesktop.org"
        },
        {
          "type": "distribution",
          "url": "https://xcb.freedesktop.org/dist/"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/littlecms2",
      "type": "library",
      "name": "Little CMS 2",
      "version": "2.19.1",
      "scope": "optional",
      "description": "Colour management (optional, used by PIL._imagingcms).",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://www.littlecms.com"
        },
        {
          "type": "distribution",
          "url": "https://github.com/mm2/Little-CMS/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/openjpeg",
      "type": "library",
      "name": "OpenJPEG",
      "version": "2.5.4",
      "scope": "optional",
      "description": "JPEG 2000 codec (optional).",
      "licenses": [
        {
          "license": {
            "id": "BSD-2-Clause"
          }
        }
      ],
      "pedigree": {
        "ancestors": [
          {
            "bom-ref": "pkg:generic/openjpeg@2.5.4#upstream",
            "type": "library",
            "name": "libtiff",
            "version": "2.5.4",
            "purl": "pkg:generic/openjpeg@2.5.4",
            "externalReferences": [
              {
                "type": "distribution",
                "url": "https://github.com/uclouvain/openjpeg/releases/tag/v2.5.4"
              }
            ]
          }
        ],
        "patches": [
          {
            "type": "cherry-pick",
            "diff": {
              "text": {
                "content": "Y29tbWl0IDkxZDA4YjExYTcyNzY0ZjZkMTk5ZjMyZmEwYzFiMWFiZDRlZGMyYWQKQXV0aG9yOiBQR1pYQiA8cGd6eGJAcXEuY29tPgpEYXRlOiAgIFR1ZSBGZWIgMTAgMTc6MDk6MzAgMjAyNiArMDAwMAoKICAgIEZpeCBoZWFwIGJ1ZmZlciBvdmVybGZvdyBpbiBvcGpfajJrX3JlYWRfc29kCgpkaWZmIC0tZ2l0IGEvc3JjL2xpYi9vcGVuanAyL2oyay5jIGIvc3JjL2xpYi9vcGVuanAyL2oyay5jCmluZGV4IGEyMDE0Yzg5Li5hZDc2YWNhNyAxMDA2NDQKLS0tIHNyYy9saWIvb3BlbmpwMi9qMmsuYworKysgc3JjL2xpYi9vcGVuanAyL2oyay5jCkBAIC01MDgyLDEyICs1MDgyLDE0IEBAIHN0YXRpYyBPUEpfQk9PTCBvcGpfajJrX3JlYWRfc29kKG9wal9qMmtfdCAqcF9qMmssCgogICAgICAgICBPUEpfVUlOVDMyIGxfY3VycmVudF90aWxlX3BhcnQgPQogICAgICAgICAgICAgbF9jc3RyX2luZGV4LT50aWxlX2luZGV4W3BfajJrLT5tX2N1cnJlbnRfdGlsZV9udW1iZXJdLmN1cnJlbnRfdHBzbm87Ci0gICAgICAgIGxfY3N0cl9pbmRleC0+dGlsZV9pbmRleFtwX2oyay0+bV9jdXJyZW50X3RpbGVfbnVtYmVyXS50cF9pbmRleFtsX2N1cnJlbnRfdGlsZV9wYXJ0XS5lbmRfaGVhZGVyCi0gICAgICAgICAgICA9Ci0gICAgICAgICAgICAgICAgbF9jdXJyZW50X3BvczsKLSAgICAgICAgbF9jc3RyX2luZGV4LT50aWxlX2luZGV4W3BfajJrLT5tX2N1cnJlbnRfdGlsZV9udW1iZXJdLnRwX2luZGV4W2xfY3VycmVudF90aWxlX3BhcnRdLmVuZF9wb3MKLSAgICAgICAgICAgID0KLSAgICAgICAgICAgICAgICBsX2N1cnJlbnRfcG9zICsgcF9qMmstPm1fc3BlY2lmaWNfcGFyYW0ubV9kZWNvZGVyLm1fc290X2xlbmd0aCArIDI7CisgICAgICAgIGlmIChsX2NzdHJfaW5kZXgtPnRpbGVfaW5kZXhbcF9qMmstPm1fY3VycmVudF90aWxlX251bWJlcl0udHBfaW5kZXggJiYKKyAgICAgICAgICAgICAgICBsX2N1cnJlbnRfdGlsZV9wYXJ0IDwKKyAgICAgICAgICAgICAgICBsX2NzdHJfaW5kZXgtPnRpbGVfaW5kZXhbcF9qMmstPm1fY3VycmVudF90aWxlX251bWJlcl0ubmJfdHBzKSB7CisgICAgICAgICAgICBsX2NzdHJfaW5kZXgtPnRpbGVfaW5kZXhbcF9qMmstPm1fY3VycmVudF90aWxlX251bWJlcl0udHBfaW5kZXhbbF9jdXJyZW50X3RpbGVfcGFydF0uZW5kX2hlYWRlcgorICAgICAgICAgICAgICAgID0gbF9jdXJyZW50X3BvczsKKyAgICAgICAgICAgIGxfY3N0cl9pbmRleC0+dGlsZV9pbmRleFtwX2oyay0+bV9jdXJyZW50X3RpbGVfbnVtYmVyXS50cF9pbmRleFtsX2N1cnJlbnRfdGlsZV9wYXJ0XS5lbmRfcG9zCisgICAgICAgICAgICAgICAgPSBsX2N1cnJlbnRfcG9zICsgcF9qMmstPm1fc3BlY2lmaWNfcGFyYW0ubV9kZWNvZGVyLm1fc290X2xlbmd0aCArIDI7CisgICAgICAgIH0KCiAgICAgICAgIGlmIChPUEpfRkFMU0UgPT0gb3BqX2oya19hZGRfdGxtYXJrZXIocF9qMmstPm1fY3VycmVudF90aWxlX251bWJlciwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBsX2NzdHJfaW5kZXgsCg==",
                "encoding": "base64"
              }
            }
          }
        ],
        "notes": "Vendored from upstream openjpeg 2.5.4 with a commit from master cherry-picked to fix OSV-2025-219."
      },
      "externalReferences": [
        {
          "type": "website",
          "url": "https://www.openjpeg.org"
        },
        {
          "type": "distribution",
          "url": "https://github.com/uclouvain/openjpeg/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:pypi/pybind11",
      "type": "library",
      "name": "pybind11",
      "scope": "excluded",
      "description": "Parallel C compilation library (build-time dependency).",
      "licenses": [
        {
          "license": {
            "id": "BSD-3-Clause"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://pybind11.readthedocs.io"
        },
        {
          "type": "distribution",
          "url": "https://github.com/pybind/pybind11/releases"
        }
      ]
    },
    {
      "bom-ref": "pkg:generic/zlib",
      "type": "library",
      "name": "zlib",
      "version": "2.3.3",
      "description": "Deflate/PNG compression (required by default; disable with -C zlib=disable).",
      "licenses": [
        {
          "license": {
            "id": "Zlib"
          }
        }
      ],
      "externalReferences": [
        {
          "type": "website",
          "url": "https://zlib.net"
        },
        {
          "type": "distribution",
          "url": "https://zlib.net"
        }
      ]
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:pypi/pillow@13.0.0",
      "dependsOn": [
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._avif",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._imaging",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingcms",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingft",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingmath",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingmorph",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingtk",
        "pkg:pypi/pillow@13.0.0#c-ext/PIL._webp"
      ]
    },
    {
      "ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._avif",
      "dependsOn": [
        "pkg:generic/libavif"
      ]
    },
    {
      "ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imaging",
      "dependsOn": [
        "pkg:generic/libimagequant",
        "pkg:generic/libjpeg",
        "pkg:generic/libtiff",
        "pkg:generic/libxcb",
        "pkg:generic/openjpeg",
        "pkg:generic/zlib"
      ]
    },
    {
      "ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingcms",
      "dependsOn": [
        "pkg:generic/littlecms2"
      ]
    },
    {
      "ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._imagingft",
      "dependsOn": [
        "pkg:generic/freetype2",
        "pkg:generic/fribidi",
        "pkg:generic/harfbuzz",
        "pkg:pypi/pillow@13.0.0#thirdparty/fribidi-shim",
        "pkg:pypi/pillow@13.0.0#thirdparty/raqm"
      ]
    },
    {
      "ref": "pkg:pypi/pillow@13.0.0#c-ext/PIL._webp",
      "dependsOn": [
        "pkg:generic/libwebp"
      ]
    },
    {
      "ref": "pkg:pypi/pillow@13.0.0#thirdparty/raqm",
      "dependsOn": [
        "pkg:generic/harfbuzz",
        "pkg:pypi/pillow@13.0.0#thirdparty/fribidi-shim"
      ]
    }
  ]
}
```

## Pygame — 2.6.1

License: LGPL-2.1-or-later

Upstream: https://www.pygame.org/

Pygame is used for optional checkout audio. Complete corresponding source, application source and rebuild instructions accompany the app. The unused FreeSans font is excluded.

### licenses/python-pygame/README.rst

```text
.. image:: https://raw.githubusercontent.com/pygame/pygame/main/docs/reST/_static/pygame_logo.svg
  :alt: pygame
  :target: https://www.pygame.org/


|AppVeyorBuild| |PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

Pygame_ is a free and open-source cross-platform library
for the development of multimedia applications like video games using Python.
It uses the `Simple DirectMedia Layer library`_ and several other
popular libraries to abstract the most common functions, making writing
these programs a more intuitive task.

`We need your help`_ to make pygame the best it can be!
New contributors are welcome.


Installation
------------

Before installing pygame, you must check that Python is installed
on your machine. To find out, open a command prompt (if you have
Windows) or a terminal (if you have MacOS or Linux) and type this:
::

   python --version


If a message such as "Python 3.8.10" appears, it means that Python
is correctly installed. If an error message appears, it means that
it is not installed yet. You must then go to the `official website
<https://www.python.org/downloads/>`_ to download it.

Once Python is installed, you have to perform a final check: you have
to see if pip is installed. Generally, pip is pre-installed with
Python but we are never sure. Same as for Python, type the following
command:
::

   pip --version


If a message such as "pip 20.0.2 from /usr/lib/python3/dist-packages/pip
(python 3.8)" appears, you are ready to install pygame! To install
it, enter this command:
::

   pip install pygame

Once pygame is installed, quickly test your library by entering the following
command, which opens one of the many example games that comes pre-installed: 
::

	python3 -m pygame.examples.aliens


If this doesn’t work, the `Getting Started 
<https://www.pygame.org/wiki/GettingStarted/>`_ section of the official 
website has more information for platform specific issues, such as adding
python to your machine’s PATH settings


Help
----

If you are just getting started with pygame, you should be able to
get started fairly quickly.  Pygame comes with many tutorials and
introductions.  There is also full reference documentation for the
entire library. Browse the documentation on the `docs page`_. You
can also browse the documentation locally by running
``python -m pygame.docs`` in your terminal. If the docs aren't found
locally, it'll launch the online website instead.

The online documentation stays up to date with the development version
of pygame on GitHub.  This may be a bit newer than the version of pygame
you are using. To upgrade to the latest full release, run
``pip install pygame --upgrade`` in your terminal.

Best of all, the examples directory has many playable small programs
which can get you started playing with the code right away.


Features
----------

Pygame is a powerful library for game development, offering a wide
range of features to simplify your coding journey. Let's delve into
what pygame has to offer:

Graphics - With pygame, creating dynamic and engaging graphics has
never been easier. The library provides simple yet effective tools for
2D graphics and animation, including support for images, rectangles,
and polygon shapes. Whether you're a seasoned game developer or just
starting out, pygame has you covered.

Sound - Pygame also includes support for playing and manipulating sound
and music, making it easy to add sound effects and background music to
your games. With support for WAV, MP3, and OGG file formats, you have
plenty of options to choose from.

Input - Pygame provides intuitive functions for handling keyboard, mouse,
and joystick input, allowing you to quickly and easily implement player
controls in your games. No more struggling with complex input code, pygame
makes it simple.

Game Development - Lastly, pygame provides a comprehensive suite of tools
and features specifically designed for game development. From collision
detection to sprite management, pygame has everything you need to create
exciting and engaging games. Whether you're building a platformer, puzzle
game, or anything in between, pygame has you covered.


Building From Source
--------------------

If you want to use features that are currently in development,
or you want to contribute to pygame, you will need to build pygame
locally from its source code, rather than pip installing it.

Installing from source is fairly automated. The most work will
involve compiling and installing all the pygame dependencies.  Once
that is done, run the ``setup.py`` script which will attempt to
auto-configure, build, and install pygame.

Much more information about installing and compiling is available
on the `Compilation wiki page`_.

Contribute
----------

* `Documentation Contributions <https://github.com/pygame/pygame/tree/main/docs>`_ - Guidelines for contributing to the main documentations
* `Writing your first unit test <http://renesd.blogspot.com/2019/11/draft-2-of-lets-write-unit-test.html>`_ - Step by step guide on how to write your first unit test in Python for Pygame.
* `How to Hack Pygame <https://www.pygame.org/wiki/Hacking>`_ - Information on hacking, developing, and modifying Pygame
* `Issue Tracker for beginners <https://github.com/pygame/pygame/labels/good%20first%20issue>`_ - A way for beginners to contribute to the project
* `Bugs & Patches <https://www.pygame.org/wiki/patchesandbugs>`_ - Report bugs
* `Communication tools <https://www.pygame.org/wiki/info>`_ - More information and ways to get in touch with the Pygame team


Credits
-------

Thanks to everyone who has helped contribute to this library.
Special thanks are also in order.

* Marcus Von Appen: many changes, and fixes, 1.7.1+ freebsd maintainer
* Lenard Lindstrom: the 1.8+ windows maintainer, many changes, and fixes
* Brian Fisher for svn auto builder, bug tracker and many contributions
* Rene Dudfield: many changes, and fixes, 1.7+ release manager/maintainer
* Phil Hassey for his work on the pygame.org website
* DR0ID for his work on the sprite module
* Richard Goedeken for his smoothscale function
* Ulf Ekström for his pixel perfect collision detection code
* Pete Shinners: original author
* David Clark for filling the right-hand-man position
* Ed Boraas and Francis Irving: Debian packages
* Maxim Sobolev: FreeBSD packaging
* Bob Ippolito: MacOS and OS X porting (much work!)
* Jan Ekhol, Ray Kelm, and Peter Nicolai: putting up with early design ideas
* Nat Pryce for starting our unit tests
* Dan Richter for documentation work
* TheCorruptor for his incredible logos and graphics
* Nicholas Dudfield: many test improvements
* Alex Folkner for pygame-ctypes

Thanks to those sending in patches and fixes: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

And our bug hunters above and beyond: Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

There's many more folks out there who've submitted helpful ideas, kept
this project going, and basically made our life easier.  Thanks!

Many thank you's for people making documentation comments, and adding to the
pygame.org wiki.

Also many thanks for people creating games and putting them on the
pygame.org website for others to learn from and enjoy.

Lots of thanks to James Paige for hosting the pygame bugzilla.

Also a big thanks to Roger Dingledine and the crew at SEUL.ORG for our
excellent hosting.

Dependencies
------------

Pygame is obviously strongly dependent on SDL and Python.  It also
links to and embeds several other smaller libraries.  The font
module relies on SDL_ttf, which is dependent on freetype.  The mixer
(and mixer.music) modules depend on SDL_mixer.  The image module
depends on SDL_image, which also can use libjpeg and libpng.  The
transform module has an embedded version of SDL_rotozoom for its
own rotozoom function.  The surfarray module requires the Python
NumPy package for its multidimensional numeric arrays.
Dependency versions:


+----------+------------------------+
| CPython  | >= 3.6 (Or use PyPy3)  |
+----------+------------------------+
| SDL      | >= 2.0.8               |
+----------+------------------------+
| SDL_mixer| >= 2.0.0               |
+----------+------------------------+
| SDL_image| >= 2.0.2               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.11              |
+----------+------------------------+
| SDL_gfx  | (Optional, vendored in)|
+----------+------------------------+
| NumPy    | >= 1.6.2 (Optional)    |
+----------+------------------------+



License
-------

This library is distributed under `GNU LGPL version 2.1`_, which can
be found in the file ``docs/LGPL.txt``.  We reserve the right to place
future versions of this library under a different license.

This basically means you can use pygame in any project you want,
but if you make any changes or additions to pygame itself, those
must be released with a compatible license (preferably submitted
back to the pygame project).  Closed source and commercial games are fine.

The programs in the ``examples`` subdirectory are in the public domain.

See docs/licenses for licenses of dependencies.


.. |AppVeyorBuild| image:: https://ci.appveyor.com/api/projects/status/x4074ybuobsh4myx?svg=true
   :target: https://ci.appveyor.com/project/pygame/pygame

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pygame.svg?v=1
   :target: https://pypi.python.org/pypi/pygame

.. |PyPiLicense| image:: https://img.shields.io/pypi/l/pygame.svg?v=1
   :target: https://pypi.python.org/pypi/pygame

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg?v=1

.. |GithubCommits| image:: https://img.shields.io/github/commits-since/pygame/pygame/2.1.2.svg
   :target: https://github.com/pygame/pygame/compare/2.1.2...main

.. |BlackFormatBadge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. _pygame: https://www.pygame.org
.. _Simple DirectMedia Layer library: https://www.libsdl.org
.. _We need your help: https://www.pygame.org/contribute.html
.. _Compilation wiki page: https://www.pygame.org/wiki/Compilation
.. _docs page: https://www.pygame.org/docs/
.. _GNU LGPL version 2.1: https://www.gnu.org/copyleft/lesser.html
```

### licenses/python-pygame/LGPL.txt

```text
		  GNU LESSER GENERAL PUBLIC LICENSE
		       Version 2.1, February 1999

 Copyright (C) 1991, 1999 Free Software Foundation, Inc.
     59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

[This is the first released version of the Lesser GPL.  It also counts
 as the successor of the GNU Library Public License, version 2, hence
 the version number 2.1.]

			    Preamble

  The licenses for most software are designed to take away your
freedom to share and change it.  By contrast, the GNU General Public
Licenses are intended to guarantee your freedom to share and change
free software--to make sure the software is free for all its users.

  This license, the Lesser General Public License, applies to some
specially designated software packages--typically libraries--of the
Free Software Foundation and other authors who decide to use it.  You
can use it too, but we suggest you first think carefully about whether
this license or the ordinary General Public License is the better
strategy to use in any particular case, based on the explanations below.

  When we speak of free software, we are referring to freedom of use,
not price.  Our General Public Licenses are designed to make sure that
you have the freedom to distribute copies of free software (and charge
for this service if you wish); that you receive source code or can get
it if you want it; that you can change the software and use pieces of
it in new free programs; and that you are informed that you can do
these things.

  To protect your rights, we need to make restrictions that forbid
distributors to deny you these rights or to ask you to surrender these
rights.  These restrictions translate to certain responsibilities for
you if you distribute copies of the library or if you modify it.

  For example, if you distribute copies of the library, whether gratis
or for a fee, you must give the recipients all the rights that we gave
you.  You must make sure that they, too, receive or can get the source
code.  If you link other code with the library, you must provide
complete object files to the recipients, so that they can relink them
with the library after making changes to the library and recompiling
it.  And you must show them these terms so they know their rights.

  We protect your rights with a two-step method: (1) we copyright the
library, and (2) we offer you this license, which gives you legal
permission to copy, distribute and/or modify the library.

  To protect each distributor, we want to make it very clear that
there is no warranty for the free library.  Also, if the library is
modified by someone else and passed on, the recipients should know
that what they have is not the original version, so that the original
author's reputation will not be affected by problems that might be
introduced by others.

  Finally, software patents pose a constant threat to the existence of
any free program.  We wish to make sure that a company cannot
effectively restrict the users of a free program by obtaining a
restrictive license from a patent holder.  Therefore, we insist that
any patent license obtained for a version of the library must be
consistent with the full freedom of use specified in this license.

  Most GNU software, including some libraries, is covered by the
ordinary GNU General Public License.  This license, the GNU Lesser
General Public License, applies to certain designated libraries, and
is quite different from the ordinary General Public License.  We use
this license for certain libraries in order to permit linking those
libraries into non-free programs.

  When a program is linked with a library, whether statically or using
a shared library, the combination of the two is legally speaking a
combined work, a derivative of the original library.  The ordinary
General Public License therefore permits such linking only if the
entire combination fits its criteria of freedom.  The Lesser General
Public License permits more lax criteria for linking other code with
the library.

  We call this license the "Lesser" General Public License because it
does Less to protect the user's freedom than the ordinary General
Public License.  It also provides other free software developers Less
of an advantage over competing non-free programs.  These disadvantages
are the reason we use the ordinary General Public License for many
libraries.  However, the Lesser license provides advantages in certain
special circumstances.

  For example, on rare occasions, there may be a special need to
encourage the widest possible use of a certain library, so that it becomes
a de-facto standard.  To achieve this, non-free programs must be
allowed to use the library.  A more frequent case is that a free
library does the same job as widely used non-free libraries.  In this
case, there is little to gain by limiting the free library to free
software only, so we use the Lesser General Public License.

  In other cases, permission to use a particular library in non-free
programs enables a greater number of people to use a large body of
free software.  For example, permission to use the GNU C Library in
non-free programs enables many more people to use the whole GNU
operating system, as well as its variant, the GNU/Linux operating
system.

  Although the Lesser General Public License is Less protective of the
users' freedom, it does ensure that the user of a program that is
linked with the Library has the freedom and the wherewithal to run
that program using a modified version of the Library.

  The precise terms and conditions for copying, distribution and
modification follow.  Pay close attention to the difference between a
"work based on the library" and a "work that uses the library".  The
former contains code derived from the library, whereas the latter must
be combined with the library in order to run.

		  GNU LESSER GENERAL PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. This License Agreement applies to any software library or other
program which contains a notice placed by the copyright holder or
other authorized party saying it may be distributed under the terms of
this Lesser General Public License (also called "this License").
Each licensee is addressed as "you".

  A "library" means a collection of software functions and/or data
prepared so as to be conveniently linked with application programs
(which use some of those functions and data) to form executables.

  The "Library", below, refers to any such software library or work
which has been distributed under these terms.  A "work based on the
Library" means either the Library or any derivative work under
copyright law: that is to say, a work containing the Library or a
portion of it, either verbatim or with modifications and/or translated
straightforwardly into another language.  (Hereinafter, translation is
included without limitation in the term "modification".)

  "Source code" for a work means the preferred form of the work for
making modifications to it.  For a library, complete source code means
all the source code for all modules it contains, plus any associated
interface definition files, plus the scripts used to control compilation
and installation of the library.

  Activities other than copying, distribution and modification are not
covered by this License; they are outside its scope.  The act of
running a program using the Library is not restricted, and output from
such a program is covered only if its contents constitute a work based
on the Library (independent of the use of the Library in a tool for
writing it).  Whether that is true depends on what the Library does
and what the program that uses the Library does.
  
  1. You may copy and distribute verbatim copies of the Library's
complete source code as you receive it, in any medium, provided that
you conspicuously and appropriately publish on each copy an
appropriate copyright notice and disclaimer of warranty; keep intact
all the notices that refer to this License and to the absence of any
warranty; and distribute a copy of this License along with the
Library.

  You may charge a fee for the physical act of transferring a copy,
and you may at your option offer warranty protection in exchange for a
fee.

  2. You may modify your copy or copies of the Library or any portion
of it, thus forming a work based on the Library, and copy and
distribute such modifications or work under the terms of Section 1
above, provided that you also meet all of these conditions:

    a) The modified work must itself be a software library.

    b) You must cause the files modified to carry prominent notices
    stating that you changed the files and the date of any change.

    c) You must cause the whole of the work to be licensed at no
    charge to all third parties under the terms of this License.

    d) If a facility in the modified Library refers to a function or a
    table of data to be supplied by an application program that uses
    the facility, other than as an argument passed when the facility
    is invoked, then you must make a good faith effort to ensure that,
    in the event an application does not supply such function or
    table, the facility still operates, and performs whatever part of
    its purpose remains meaningful.

    (For example, a function in a library to compute square roots has
    a purpose that is entirely well-defined independent of the
    application.  Therefore, Subsection 2d requires that any
    application-supplied function or table used by this function must
    be optional: if the application does not supply it, the square
    root function must still compute square roots.)

These requirements apply to the modified work as a whole.  If
identifiable sections of that work are not derived from the Library,
and can be reasonably considered independent and separate works in
themselves, then this License, and its terms, do not apply to those
sections when you distribute them as separate works.  But when you
distribute the same sections as part of a whole which is a work based
on the Library, the distribution of the whole must be on the terms of
this License, whose permissions for other licensees extend to the
entire whole, and thus to each and every part regardless of who wrote
it.

Thus, it is not the intent of this section to claim rights or contest
your rights to work written entirely by you; rather, the intent is to
exercise the right to control the distribution of derivative or
collective works based on the Library.

In addition, mere aggregation of another work not based on the Library
with the Library (or with a work based on the Library) on a volume of
a storage or distribution medium does not bring the other work under
the scope of this License.

  3. You may opt to apply the terms of the ordinary GNU General Public
License instead of this License to a given copy of the Library.  To do
this, you must alter all the notices that refer to this License, so
that they refer to the ordinary GNU General Public License, version 2,
instead of to this License.  (If a newer version than version 2 of the
ordinary GNU General Public License has appeared, then you can specify
that version instead if you wish.)  Do not make any other change in
these notices.

  Once this change is made in a given copy, it is irreversible for
that copy, so the ordinary GNU General Public License applies to all
subsequent copies and derivative works made from that copy.

  This option is useful when you wish to copy part of the code of
the Library into a program that is not a library.

  4. You may copy and distribute the Library (or a portion or
derivative of it, under Section 2) in object code or executable form
under the terms of Sections 1 and 2 above provided that you accompany
it with the complete corresponding machine-readable source code, which
must be distributed under the terms of Sections 1 and 2 above on a
medium customarily used for software interchange.

  If distribution of object code is made by offering access to copy
from a designated place, then offering equivalent access to copy the
source code from the same place satisfies the requirement to
distribute the source code, even though third parties are not
compelled to copy the source along with the object code.

  5. A program that contains no derivative of any portion of the
Library, but is designed to work with the Library by being compiled or
linked with it, is called a "work that uses the Library".  Such a
work, in isolation, is not a derivative work of the Library, and
therefore falls outside the scope of this License.

  However, linking a "work that uses the Library" with the Library
creates an executable that is a derivative of the Library (because it
contains portions of the Library), rather than a "work that uses the
library".  The executable is therefore covered by this License.
Section 6 states terms for distribution of such executables.

  When a "work that uses the Library" uses material from a header file
that is part of the Library, the object code for the work may be a
derivative work of the Library even though the source code is not.
Whether this is true is especially significant if the work can be
linked without the Library, or if the work is itself a library.  The
threshold for this to be true is not precisely defined by law.

  If such an object file uses only numerical parameters, data
structure layouts and accessors, and small macros and small inline
functions (ten lines or less in length), then the use of the object
file is unrestricted, regardless of whether it is legally a derivative
work.  (Executables containing this object code plus portions of the
Library will still fall under Section 6.)

  Otherwise, if the work is a derivative of the Library, you may
distribute the object code for the work under the terms of Section 6.
Any executables containing that work also fall under Section 6,
whether or not they are linked directly with the Library itself.

  6. As an exception to the Sections above, you may also combine or
link a "work that uses the Library" with the Library to produce a
work containing portions of the Library, and distribute that work
under terms of your choice, provided that the terms permit
modification of the work for the customer's own use and reverse
engineering for debugging such modifications.

  You must give prominent notice with each copy of the work that the
Library is used in it and that the Library and its use are covered by
this License.  You must supply a copy of this License.  If the work
during execution displays copyright notices, you must include the
copyright notice for the Library among them, as well as a reference
directing the user to the copy of this License.  Also, you must do one
of these things:

    a) Accompany the work with the complete corresponding
    machine-readable source code for the Library including whatever
    changes were used in the work (which must be distributed under
    Sections 1 and 2 above); and, if the work is an executable linked
    with the Library, with the complete machine-readable "work that
    uses the Library", as object code and/or source code, so that the
    user can modify the Library and then relink to produce a modified
    executable containing the modified Library.  (It is understood
    that the user who changes the contents of definitions files in the
    Library will not necessarily be able to recompile the application
    to use the modified definitions.)

    b) Use a suitable shared library mechanism for linking with the
    Library.  A suitable mechanism is one that (1) uses at run time a
    copy of the library already present on the user's computer system,
    rather than copying library functions into the executable, and (2)
    will operate properly with a modified version of the library, if
    the user installs one, as long as the modified version is
    interface-compatible with the version that the work was made with.

    c) Accompany the work with a written offer, valid for at
    least three years, to give the same user the materials
    specified in Subsection 6a, above, for a charge no more
    than the cost of performing this distribution.

    d) If distribution of the work is made by offering access to copy
    from a designated place, offer equivalent access to copy the above
    specified materials from the same place.

    e) Verify that the user has already received a copy of these
    materials or that you have already sent this user a copy.

  For an executable, the required form of the "work that uses the
Library" must include any data and utility programs needed for
reproducing the executable from it.  However, as a special exception,
the materials to be distributed need not include anything that is
normally distributed (in either source or binary form) with the major
components (compiler, kernel, and so on) of the operating system on
which the executable runs, unless that component itself accompanies
the executable.

  It may happen that this requirement contradicts the license
restrictions of other proprietary libraries that do not normally
accompany the operating system.  Such a contradiction means you cannot
use both them and the Library together in an executable that you
distribute.

  7. You may place library facilities that are a work based on the
Library side-by-side in a single library together with other library
facilities not covered by this License, and distribute such a combined
library, provided that the separate distribution of the work based on
the Library and of the other library facilities is otherwise
permitted, and provided that you do these two things:

    a) Accompany the combined library with a copy of the same work
    based on the Library, uncombined with any other library
    facilities.  This must be distributed under the terms of the
    Sections above.

    b) Give prominent notice with the combined library of the fact
    that part of it is a work based on the Library, and explaining
    where to find the accompanying uncombined form of the same work.

  8. You may not copy, modify, sublicense, link with, or distribute
the Library except as expressly provided under this License.  Any
attempt otherwise to copy, modify, sublicense, link with, or
distribute the Library is void, and will automatically terminate your
rights under this License.  However, parties who have received copies,
or rights, from you under this License will not have their licenses
terminated so long as such parties remain in full compliance.

  9. You are not required to accept this License, since you have not
signed it.  However, nothing else grants you permission to modify or
distribute the Library or its derivative works.  These actions are
prohibited by law if you do not accept this License.  Therefore, by
modifying or distributing the Library (or any work based on the
Library), you indicate your acceptance of this License to do so, and
all its terms and conditions for copying, distributing or modifying
the Library or works based on it.

  10. Each time you redistribute the Library (or any work based on the
Library), the recipient automatically receives a license from the
original licensor to copy, distribute, link with or modify the Library
subject to these terms and conditions.  You may not impose any further
restrictions on the recipients' exercise of the rights granted herein.
You are not responsible for enforcing compliance by third parties with
this License.

  11. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot
distribute so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you
may not distribute the Library at all.  For example, if a patent
license would not permit royalty-free redistribution of the Library by
all those who receive copies directly or indirectly through you, then
the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Library.

If any portion of this section is held invalid or unenforceable under any
particular circumstance, the balance of the section is intended to apply,
and the section as a whole is intended to apply in other circumstances.

It is not the purpose of this section to induce you to infringe any
patents or other property right claims or to contest validity of any
such claims; this section has the sole purpose of protecting the
integrity of the free software distribution system which is
implemented by public license practices.  Many people have made
generous contributions to the wide range of software distributed
through that system in reliance on consistent application of that
system; it is up to the author/donor to decide if he or she is willing
to distribute software through any other system and a licensee cannot
impose that choice.

This section is intended to make thoroughly clear what is believed to
be a consequence of the rest of this License.

  12. If the distribution and/or use of the Library is restricted in
certain countries either by patents or by copyrighted interfaces, the
original copyright holder who places the Library under this License may add
an explicit geographical distribution limitation excluding those countries,
so that distribution is permitted only in or among countries not thus
excluded.  In such case, this License incorporates the limitation as if
written in the body of this License.

  13. The Free Software Foundation may publish revised and/or new
versions of the Lesser General Public License from time to time.
Such new versions will be similar in spirit to the present version,
but may differ in detail to address new problems or concerns.

Each version is given a distinguishing version number.  If the Library
specifies a version number of this License which applies to it and
"any later version", you have the option of following the terms and
conditions either of that version or of any later version published by
the Free Software Foundation.  If the Library does not specify a
license version number, you may choose any version ever published by
the Free Software Foundation.

  14. If you wish to incorporate parts of the Library into other free
programs whose distribution conditions are incompatible with these,
write to the author to ask for permission.  For software which is
copyrighted by the Free Software Foundation, write to the Free
Software Foundation; we sometimes make exceptions for this.  Our
decision will be guided by the two goals of preserving the free status
of all derivatives of our free software and of promoting the sharing
and reuse of software generally.

			    NO WARRANTY

  15. BECAUSE THE LIBRARY IS LICENSED FREE OF CHARGE, THERE IS NO
WARRANTY FOR THE LIBRARY, TO THE EXTENT PERMITTED BY APPLICABLE LAW.
EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR
OTHER PARTIES PROVIDE THE LIBRARY "AS IS" WITHOUT WARRANTY OF ANY
KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE
LIBRARY IS WITH YOU.  SHOULD THE LIBRARY PROVE DEFECTIVE, YOU ASSUME
THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN
WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY
AND/OR REDISTRIBUTE THE LIBRARY AS PERMITTED ABOVE, BE LIABLE TO YOU
FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE
LIBRARY (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING
RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A
FAILURE OF THE LIBRARY TO OPERATE WITH ANY OTHER SOFTWARE), EVEN IF
SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGES.

		     END OF TERMS AND CONDITIONS

           How to Apply These Terms to Your New Libraries

  If you develop a new library, and you want it to be of the greatest
possible use to the public, we recommend making it free software that
everyone can redistribute and change.  You can do so by permitting
redistribution under these terms (or, alternatively, under the terms of the
ordinary General Public License).

  To apply these terms, attach the following notices to the library.  It is
safest to attach them to the start of each source file to most effectively
convey the exclusion of warranty; and each file should have at least the
"copyright" line and a pointer to where the full notice is found.

    <one line to give the library's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Also add information on how to contact you by electronic and paper mail.

You should also get your employer (if you work as a programmer) or your
school, if any, to sign a "copyright disclaimer" for the library, if
necessary.  Here is a sample; alter the names:

  Yoyodyne, Inc., hereby disclaims all copyright interest in the
  library `Frob' (a library for tweaking knobs) written by James Random Hacker.

  <signature of Ty Coon>, 1 April 1990
  Ty Coon, President of Vice

That's all there is to it!
```

### licenses/python-pygame/LICENSE.sdl_gfx.txt

```text
SDL_gfx COPYING

Library is governed under the ZLib license.

http://www.zlib.net/zlib_license.html

(C) A. Schiffler, aschiffler [at] ferzkopp.net 2012-2018, licensed under the zlib license
```

### licenses/python-pygame/LICENSE.sse2neon-h.txt

```text
// This header file provides a simple API translation layer
// between SSE intrinsics to their corresponding Arm/Aarch64 NEON versions
//
// This header file does not yet translate all of the SSE intrinsics.
//
// Contributors to this work are:
//   John W. Ratcliff <jratcliffscarab@gmail.com>
//   Brandon Rowlett <browlett@nvidia.com>
//   Ken Fast <kfast@gdeb.com>
//   Eric van Beurden <evanbeurden@nvidia.com>
//   Alexander Potylitsin <apotylitsin@nvidia.com>
//   Hasindu Gamaarachchi <hasindu2008@gmail.com>
//   Jim Huang <jserv@biilabs.io>
//   Mark Cheng <marktwtn@biilabs.io>
//   Malcolm James MacLeod <malcolm@gulden.com>
//   Devin Hussey (easyaspi314) <husseydevin@gmail.com>
//   Sebastian Pop <spop@amazon.com>

/*
 * The MIT license:
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
```

## pyinstaller — 6.22.3

License: GPLv2-or-later with a special exception which allows to use PyInstaller to build and distribute non-free programs (including commercial ones)

Upstream: https://pyinstaller.org/en/stable/license.html

### licenses/python-pyinstaller/COPYING.txt

```text
================================
 The PyInstaller licensing terms
================================
 

Copyright (c) 2010-2023, PyInstaller Development Team
Copyright (c) 2005-2009, Giovanni Bajo
Based on previous work under copyright (c) 2002 McMillan Enterprises, Inc.


PyInstaller is licensed under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.


Bootloader Exception
--------------------

In addition to the permissions in the GNU General Public License, the
authors give you unlimited permission to link or embed compiled bootloader
and related files into combinations with other programs, and to distribute
those combinations without any restriction coming from the use of those
files. (The General Public License restrictions do apply in other respects;
for example, they cover modification of the files, and distribution when
not linked into a combined executable.)
 
 
Bootloader and Related Files
----------------------------

Bootloader and related files are files which are embedded within the
final executable. This includes files in directories:

./bootloader/
./PyInstaller/loader


Run-time Hooks
----------------------------

Run-time Hooks are a different kind of files embedded within the final
executable. To ease moving them into a separate repository, or into the
respective project, these files are now licensed under the Apache License,
Version 2.0.

Run-time Hooks are in the directory
./PyInstaller/hooks/rthooks


Additional Run-time Modules
----------------------------------

In addition to run-time hooks, PyInstaller may embed additional run-time
modules in the final executable. At the time of writing, these include
the splash-screen module (``pyi_splash``) and modules from utility package
for run-time hooks (``_pyi_rth_utils``). All these files are licensed under
the Apache License, Version 2.0, and are located in the following directory:

./PyInstaller/fake-modules


The PyInstaller.isolated submodule
----------------------------------

By request, the PyInstaller.isolated submodule and its corresponding tests are
additionally licensed with the MIT license so that it may be reused outside of
PyInstaller under GPL 2.0 or MIT terms and conditions -- whichever is the most
suitable to the recipient downstream project. Affected files/directories are:

./PyInstaller/isolated/
./tests/unit/test_isolation.py


About the PyInstaller Development Team
--------------------------------------

The PyInstaller Development Team is the set of contributors
to the PyInstaller project. A full list with details is kept
in the documentation directory, in the file
``doc/CREDITS.rst``.

The core team that coordinates development on GitHub can be found here:
https://github.com/pyinstaller/pyinstaller.  As of 2021, it consists of:

* Hartmut Goebel
* Jasper Harrison
* Bryan Jones
* Brenainn Woodsend
* Rok Mandeljc

Our Copyright Policy
--------------------

PyInstaller uses a shared copyright model. Each contributor maintains copyright
over their contributions to PyInstaller. But, it is important to note that these
contributions are typically only changes to the repositories. Thus,
the PyInstaller source code, in its entirety is not the copyright of any single
person or institution.  Instead, it is the collective copyright of the entire
PyInstaller Development Team.  If individual contributors want to maintain
a record of what changes/contributions they have specific copyright on, they
should indicate their copyright in the commit message of the change, when they
commit the change to the PyInstaller repository.

With this in mind, the following banner should be used in any source code file
to indicate the copyright and license terms:


#-----------------------------------------------------------------------------
# Copyright (c) 2005-2023, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------


For run-time hooks, the following banner should be used:

#-----------------------------------------------------------------------------
# Copyright (c) 2005-2023, PyInstaller Development Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: Apache-2.0
#-----------------------------------------------------------------------------


================================
GNU General Public License
================================

https://gnu.org/licenses/gpl-2.0.html


		    GNU GENERAL PUBLIC LICENSE
		       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.
 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

			    Preamble

  The licenses for most software are designed to take away your
freedom to share and change it.  By contrast, the GNU General Public
License is intended to guarantee your freedom to share and change free
software--to make sure the software is free for all its users.  This
General Public License applies to most of the Free Software
Foundation's software and to any other program whose authors commit to
using it.  (Some other Free Software Foundation software is covered by
the GNU Library General Public License instead.)  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
this service if you wish), that you receive source code or can get it
if you want it, that you can change the software or use pieces of it
in new free programs; and that you know you can do these things.

  To protect your rights, we need to make restrictions that forbid
anyone to deny you these rights or to ask you to surrender the rights.
These restrictions translate to certain responsibilities for you if you
distribute copies of the software, or if you modify it.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must give the recipients all the rights that
you have.  You must make sure that they, too, receive or can get the
source code.  And you must show them these terms so they know their
rights.

  We protect your rights with two steps: (1) copyright the software, and
(2) offer you this license which gives you legal permission to copy,
distribute and/or modify the software.

  Also, for each author's protection and ours, we want to make certain
that everyone understands that there is no warranty for this free
software.  If the software is modified by someone else and passed on, we
want its recipients to know that what they have is not the original, so
that any problems introduced by others will not reflect on the original
authors' reputations.

  Finally, any free program is threatened constantly by software
patents.  We wish to avoid the danger that redistributors of a free
program will individually obtain patent licenses, in effect making the
program proprietary.  To prevent this, we have made it clear that any
patent must be licensed for everyone's free use or not licensed at all.

  The precise terms and conditions for copying, distribution and
modification follow.

		    GNU GENERAL PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. This License applies to any program or other work which contains
a notice placed by the copyright holder saying it may be distributed
under the terms of this General Public License.  The "Program", below,
refers to any such program or work, and a "work based on the Program"
means either the Program or any derivative work under copyright law:
that is to say, a work containing the Program or a portion of it,
either verbatim or with modifications and/or translated into another
language.  (Hereinafter, translation is included without limitation in
the term "modification".)  Each licensee is addressed as "you".

Activities other than copying, distribution and modification are not
covered by this License; they are outside its scope.  The act of
running the Program is not restricted, and the output from the Program
is covered only if its contents constitute a work based on the
Program (independent of having been made by running the Program).
Whether that is true depends on what the Program does.

  1. You may copy and distribute verbatim copies of the Program's
source code as you receive it, in any medium, provided that you
conspicuously and appropriately publish on each copy an appropriate
copyright notice and disclaimer of warranty; keep intact all the
notices that refer to this License and to the absence of any warranty;
and give any other recipients of the Program a copy of this License
along with the Program.

You may charge a fee for the physical act of transferring a copy, and
you may at your option offer warranty protection in exchange for a fee.

  2. You may modify your copy or copies of the Program or any portion
of it, thus forming a work based on the Program, and copy and
distribute such modifications or work under the terms of Section 1
above, provided that you also meet all of these conditions:

    a) You must cause the modified files to carry prominent notices
    stating that you changed the files and the date of any change.

    b) You must cause any work that you distribute or publish, that in
    whole or in part contains or is derived from the Program or any
    part thereof, to be licensed as a whole at no charge to all third
    parties under the terms of this License.

    c) If the modified program normally reads commands interactively
    when run, you must cause it, when started running for such
    interactive use in the most ordinary way, to print or display an
    announcement including an appropriate copyright notice and a
    notice that there is no warranty (or else, saying that you provide
    a warranty) and that users may redistribute the program under
    these conditions, and telling the user how to view a copy of this
    License.  (Exception: if the Program itself is interactive but
    does not normally print such an announcement, your work based on
    the Program is not required to print an announcement.)

These requirements apply to the modified work as a whole.  If
identifiable sections of that work are not derived from the Program,
and can be reasonably considered independent and separate works in
themselves, then this License, and its terms, do not apply to those
sections when you distribute them as separate works.  But when you
distribute the same sections as part of a whole which is a work based
on the Program, the distribution of the whole must be on the terms of
this License, whose permissions for other licensees extend to the
entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest
your rights to work written entirely by you; rather, the intent is to
exercise the right to control the distribution of derivative or
collective works based on the Program.

In addition, mere aggregation of another work not based on the Program
with the Program (or with a work based on the Program) on a volume of
a storage or distribution medium does not bring the other work under
the scope of this License.

  3. You may copy and distribute the Program (or a work based on it,
under Section 2) in object code or executable form under the terms of
Sections 1 and 2 above provided that you also do one of the following:

    a) Accompany it with the complete corresponding machine-readable
    source code, which must be distributed under the terms of Sections
    1 and 2 above on a medium customarily used for software interchange; or,

    b) Accompany it with a written offer, valid for at least three
    years, to give any third party, for a charge no more than your
    cost of physically performing source distribution, a complete
    machine-readable copy of the corresponding source code, to be
    distributed under the terms of Sections 1 and 2 above on a medium
    customarily used for software interchange; or,

    c) Accompany it with the information you received as to the offer
    to distribute corresponding source code.  (This alternative is
    allowed only for noncommercial distribution and only if you
    received the program in object code or executable form with such
    an offer, in accord with Subsection b above.)

The source code for a work means the preferred form of the work for
making modifications to it.  For an executable work, complete source
code means all the source code for all modules it contains, plus any
associated interface definition files, plus the scripts used to
control compilation and installation of the executable.  However, as a
special exception, the source code distributed need not include
anything that is normally distributed (in either source or binary
form) with the major components (compiler, kernel, and so on) of the
operating system on which the executable runs, unless that component
itself accompanies the executable.

If distribution of executable or object code is made by offering
access to copy from a designated place, then offering equivalent
access to copy the source code from the same place counts as
distribution of the source code, even though third parties are not
compelled to copy the source along with the object code.

  4. You may not copy, modify, sublicense, or distribute the Program
except as expressly provided under this License.  Any attempt
otherwise to copy, modify, sublicense or distribute the Program is
void, and will automatically terminate your rights under this License.
However, parties who have received copies, or rights, from you under
this License will not have their licenses terminated so long as such
parties remain in full compliance.

  5. You are not required to accept this License, since you have not
signed it.  However, nothing else grants you permission to modify or
distribute the Program or its derivative works.  These actions are
prohibited by law if you do not accept this License.  Therefore, by
modifying or distributing the Program (or any work based on the
Program), you indicate your acceptance of this License to do so, and
all its terms and conditions for copying, distributing or modifying
the Program or works based on it.

  6. Each time you redistribute the Program (or any work based on the
Program), the recipient automatically receives a license from the
original licensor to copy, distribute or modify the Program subject to
these terms and conditions.  You may not impose any further
restrictions on the recipients' exercise of the rights granted herein.
You are not responsible for enforcing compliance by third parties to
this License.

  7. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot
distribute so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you
may not distribute the Program at all.  For example, if a patent
license would not permit royalty-free redistribution of the Program by
all those who receive copies directly or indirectly through you, then
the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under
any particular circumstance, the balance of the section is intended to
apply and the section as a whole is intended to apply in other
circumstances.

It is not the purpose of this section to induce you to infringe any
patents or other property right claims or to contest validity of any
such claims; this section has the sole purpose of protecting the
integrity of the free software distribution system, which is
implemented by public license practices.  Many people have made
generous contributions to the wide range of software distributed
through that system in reliance on consistent application of that
system; it is up to the author/donor to decide if he or she is willing
to distribute software through any other system and a licensee cannot
impose that choice.

This section is intended to make thoroughly clear what is believed to
be a consequence of the rest of this License.

  8. If the distribution and/or use of the Program is restricted in
certain countries either by patents or by copyrighted interfaces, the
original copyright holder who places the Program under this License
may add an explicit geographical distribution limitation excluding
those countries, so that distribution is permitted only in or among
countries not thus excluded.  In such case, this License incorporates
the limitation as if written in the body of this License.

  9. The Free Software Foundation may publish revised and/or new versions
of the General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

Each version is given a distinguishing version number.  If the Program
specifies a version number of this License which applies to it and "any
later version", you have the option of following the terms and conditions
either of that version or of any later version published by the Free
Software Foundation.  If the Program does not specify a version number of
this License, you may choose any version ever published by the Free Software
Foundation.

  10. If you wish to incorporate parts of the Program into other free
programs whose distribution conditions are different, write to the author
to ask for permission.  For software which is copyrighted by the Free
Software Foundation, write to the Free Software Foundation; we sometimes
make exceptions for this.  Our decision will be guided by the two goals
of preserving the free status of all derivatives of our free software and
of promoting the sharing and reuse of software generally.

			    NO WARRANTY

  11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.

  12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.

		     END OF TERMS AND CONDITIONS

================================
Apache License 2.0
================================

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

===========
MIT License
===========

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### licenses/python-pyinstaller/RUNTIME-HOOK-NOTICES.txt

```text
pyi_rth_inspect.py
#-----------------------------------------------------------------------------
# Copyright (c) 2021-2023, PyInstaller Development Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: Apache-2.0
#-----------------------------------------------------------------------------



pyi_rth_pkgutil.py
#-----------------------------------------------------------------------------
# Copyright (c) 2021-2023, PyInstaller Development Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: Apache-2.0
#-----------------------------------------------------------------------------
#
# The run-time hook provides a custom module iteration function for our PyiFrozenFinder, which allows

pyi_rth_multiprocessing.py
#-----------------------------------------------------------------------------
# Copyright (c) 2017-2023, PyInstaller Development Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: Apache-2.0
#-----------------------------------------------------------------------------



pyi_rth__tkinter.py
#-----------------------------------------------------------------------------
# Copyright (c) 2013-2023, PyInstaller Development Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: Apache-2.0
#-----------------------------------------------------------------------------



pyiboot01_bootstrap.py
#-----------------------------------------------------------------------------
# Copyright (c) 2005-2023, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------
```

### licenses/python-pyinstaller/Apache-2.0.txt

```text

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

## reportlab — 5.1.0

License: BSD license (see license.txt for details), Copyright (c) 2000-2025, ReportLab Inc.

Upstream: https://pypi.org/project/reportlab/5.1.0/#files

### licenses/python-reportlab/LICENSE

```text
#####################################################################################
#
#	Copyright (c) 2000-2024, ReportLab Inc.
#	All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification,
#	are permitted provided that the following conditions are met:
#
#		*	Redistributions of source code must retain the above copyright notice,
#			this list of conditions and the following disclaimer. 
#		*	Redistributions in binary form must reproduce the above copyright notice,
#			this list of conditions and the following disclaimer in the documentation
#			and/or other materials provided with the distribution. 
#		*	Neither the name of the company nor the names of its contributors may be
#			used to endorse or promote products derived from this software without
#			specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#	IN NO EVENT SHALL THE OFFICERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#	INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#	TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#	OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
#	IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#	IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#	SUCH DAMAGE.
#
#####################################################################################
```

### licenses/python-reportlab/license.txt

```text
#####################################################################################
#
#	Copyright (c) 2000-2018, ReportLab Inc.
#	All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification,
#	are permitted provided that the following conditions are met:
#
#		*	Redistributions of source code must retain the above copyright notice,
#			this list of conditions and the following disclaimer. 
#		*	Redistributions in binary form must reproduce the above copyright notice,
#			this list of conditions and the following disclaimer in the documentation
#			and/or other materials provided with the distribution. 
#		*	Neither the name of the company nor the names of its contributors may be
#			used to endorse or promote products derived from this software without
#			specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#	IN NO EVENT SHALL THE OFFICERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#	INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#	TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#	OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
#	IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#	IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#	SUCH DAMAGE.
#
#####################################################################################
```

## brotli — 1.2.0-1.1

License: MIT

Upstream: https://github.com/google/brotli

### licenses/system-brotli/LICENSE

```text
Copyright (c) 2009, 2010, 2013-2016 by the Brotli Authors.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## bzip2 — 1.0.8-6.1

License: BSD

Upstream: https://sourceware.org/bzip2/

### licenses/system-bzip2/LICENSE

```text

--------------------------------------------------------------------------

This program, "bzip2", the associated library "libbzip2", and all
documentation, are copyright (C) 1996-2019 Julian R Seward.  All
rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. The origin of this software must not be misrepresented; you must 
   not claim that you wrote the original software.  If you use this 
   software in a product, an acknowledgment in the product 
   documentation would be appreciated but is not required.

3. Altered source versions must be plainly marked as such, and must
   not be misrepresented as being the original software.

4. The name of the author may not be used to endorse or promote 
   products derived from this software without specific prior written 
   permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Julian Seward, jseward@acm.org
bzip2/libbzip2 version 1.0.8 of 13 July 2019

--------------------------------------------------------------------------
```

## expat — 2.9.0-1.1

License: MIT

Upstream: https://libexpat.github.io/

### licenses/system-expat/COPYING

```text
Copyright (c) 1998-2000 Thai Open Source Software Center Ltd and Clark Cooper
Copyright (c) 2001-2025 Expat maintainers

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## fontconfig — 2:2.18.3-2.1

License: HPND AND Unicode-DFS-2016

Upstream: https://www.freedesktop.org/wiki/Software/fontconfig/

### licenses/system-fontconfig/COPYING

```text
fontconfig/COPYING

Copyright © 2000,2001,2002,2003,2004,2006,2007 Keith Packard
Copyright © 2005 Patrick Lam
Copyright © 2007 Dwayne Bailey and Translate.org.za
Copyright © 2009 Roozbeh Pournader
Copyright © 2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020 Red Hat, Inc.
Copyright © 2008 Danilo Šegan
Copyright © 2012 Google, Inc.


Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of the author(s) not be used in
advertising or publicity pertaining to distribution of the software without
specific, written prior permission.  The authors make no
representations about the suitability of this software for any purpose.  It
is provided "as is" without express or implied warranty.

THE AUTHOR(S) DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.


--------------------------------------------------------------------------------
fontconfig/fc-case/CaseFolding.txt

© 2019 Unicode®, Inc.
Unicode and the Unicode Logo are registered trademarks of Unicode, Inc. in the U.S. and other countries.
For terms of use, see http://www.unicode.org/terms_of_use.html


--------------------------------------------------------------------------------
fontconfig/src/fcatomic.h

/*
 * Mutex operations.  Originally copied from HarfBuzz.
 *
 * Copyright © 2007  Chris Wilson
 * Copyright © 2009,2010  Red Hat, Inc.
 * Copyright © 2011,2012,2013  Google, Inc.
 *
 * Permission is hereby granted, without written agreement and without
 * license or royalty fees, to use, copy, modify, and distribute this
 * software and its documentation for any purpose, provided that the
 * above copyright notice and the following two paragraphs appear in
 * all copies of this software.
 *
 * IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE TO ANY PARTY FOR
 * DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
 * ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN
 * IF THE COPYRIGHT HOLDER HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 *
 * THE COPYRIGHT HOLDER SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
 * BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
 * ON AN "AS IS" BASIS, AND THE COPYRIGHT HOLDER HAS NO OBLIGATION TO
 * PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
 *
 * Contributor(s):
 *	Chris Wilson <chris@chris-wilson.co.uk>
 * Red Hat Author(s): Behdad Esfahbod
 * Google Author(s): Behdad Esfahbod
 */


--------------------------------------------------------------------------------
fontconfig/src/fcfoundry.h

/*
  Copyright © 2002-2003 by Juliusz Chroboczek

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
*/


--------------------------------------------------------------------------------
fontconfig/src/fcmd5.h

/*
 * This code implements the MD5 message-digest algorithm.
 * The algorithm is due to Ron Rivest.  This code was
 * written by Colin Plumb in 1993, no copyright is claimed.
 * This code is in the public domain; do with it what you wish.
 *
 * Equivalent code is available from RSA Data Security, Inc.
 * This code has been tested against that, and is equivalent,
 * except that you don't need to include two pages of legalese
 * with every copy.
 *
 * To compute the message digest of a chunk of bytes, declare an
 * MD5Context structure, pass it to MD5Init, call MD5Update as
 * needed on buffers full of bytes, and then call MD5Final, which
 * will fill a supplied 16-byte array with the digest.
 */


--------------------------------------------------------------------------------
fontconfig/src/fcmutex.h

/*
 * Atomic int and pointer operations.  Originally copied from HarfBuzz.
 *
 * Copyright © 2007  Chris Wilson
 * Copyright © 2009,2010  Red Hat, Inc.
 * Copyright © 2011,2012,2013  Google, Inc.
 *
 * Permission is hereby granted, without written agreement and without
 * license or royalty fees, to use, copy, modify, and distribute this
 * software and its documentation for any purpose, provided that the
 * above copyright notice and the following two paragraphs appear in
 * all copies of this software.
 *
 * IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE TO ANY PARTY FOR
 * DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
 * ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN
 * IF THE COPYRIGHT HOLDER HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 *
 * THE COPYRIGHT HOLDER SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
 * BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
 * ON AN "AS IS" BASIS, AND THE COPYRIGHT HOLDER HAS NO OBLIGATION TO
 * PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
 *
 * Contributor(s):
 *	Chris Wilson <chris@chris-wilson.co.uk>
 * Red Hat Author(s): Behdad Esfahbod
 * Google Author(s): Behdad Esfahbod
 */


--------------------------------------------------------------------------------
fontconfig/src/ftglue.[ch]

/* ftglue.c: Glue code for compiling the OpenType code from
 *           FreeType 1 using only the public API of FreeType 2
 *
 * By David Turner, The FreeType Project (www.freetype.org)
 *
 * This code is explicitely put in the public domain
 *
 * ==========================================================================
 *
 * the OpenType parser codes was originally written as an extension to
 * FreeType 1.x. As such, its source code was embedded within the library,
 * and used many internal FreeType functions to deal with memory and
 * stream i/o.
 *
 * When it was 'salvaged' for Pango and Qt, the code was "ported" to FreeType 2,
 * which basically means that some macro tricks were performed in order to
 * directly access FT2 _internal_ functions.
 *
 * these functions were never part of FT2 public API, and _did_ change between
 * various releases. This created chaos for many users: when they upgraded the
 * FreeType library on their system, they couldn't run Gnome anymore since
 * Pango refused to link.
 *
 * Very fortunately, it's possible to completely avoid this problem because
 * the FT_StreamRec and FT_MemoryRec structure types, which describe how
 * memory and stream implementations interface with the rest of the font
 * library, have always been part of the public API, and never changed.
 *
 * What we do thus is re-implement, within the OpenType parser, the few
 * functions that depend on them. This only adds one or two kilobytes of
 * code, and ensures that the parser can work with _any_ version
 * of FreeType installed on your system. How sweet... !
 *
 * Note that we assume that Pango doesn't use any other internal functions
 * from FreeType. It used to in old versions, but this should no longer
 * be the case. (crossing my fingers).
 *
 *  - David Turner
 *  - The FreeType Project  (www.freetype.org)
 *
 * PS: This "glue" code is explicitely put in the public domain
 */
```

## freetype2 — 2.15.0-1.1

License: FTL (permitted alternative to GPL)

Upstream: https://gitlab.freedesktop.org/freetype/freetype/-/blob/master/docs/FTL.TXT

### licenses/system-freetype2/FTL.TXT

```text
                    The FreeType Project LICENSE
                    ----------------------------

                            2006-Jan-27

                    Copyright 1996-2002, 2006 by
          David Turner, Robert Wilhelm, and Werner Lemberg



Introduction
============

  The FreeType  Project is distributed in  several archive packages;
  some of them may contain, in addition to the FreeType font engine,
  various tools and  contributions which rely on, or  relate to, the
  FreeType Project.

  This  license applies  to all  files found  in such  packages, and
  which do not  fall under their own explicit  license.  The license
  affects  thus  the  FreeType   font  engine,  the  test  programs,
  documentation and makefiles, at the very least.

  This  license   was  inspired  by  the  BSD,   Artistic,  and  IJG
  (Independent JPEG  Group) licenses, which  all encourage inclusion
  and  use of  free  software in  commercial  and freeware  products
  alike.  As a consequence, its main points are that:

    o We don't promise that this software works. However, we will be
      interested in any kind of bug reports. (`as is' distribution)

    o You can  use this software for whatever you  want, in parts or
      full form, without having to pay us. (`royalty-free' usage)

    o You may not pretend that  you wrote this software.  If you use
      it, or  only parts of it,  in a program,  you must acknowledge
      somewhere  in  your  documentation  that  you  have  used  the
      FreeType code. (`credits')

  We  specifically  permit  and  encourage  the  inclusion  of  this
  software, with  or without modifications,  in commercial products.
  We  disclaim  all warranties  covering  The  FreeType Project  and
  assume no liability related to The FreeType Project.


  Finally,  many  people  asked  us  for  a  preferred  form  for  a
  credit/disclaimer to use in compliance with this license.  We thus
  encourage you to use the following text:

   """
    Portions of this software are copyright © <year> The FreeType
    Project (https://freetype.org).  All rights reserved.
   """

  Please replace <year> with the value from the FreeType version you
  actually use.


Legal Terms
===========

0. Definitions
--------------

  Throughout this license,  the terms `package', `FreeType Project',
  and  `FreeType  archive' refer  to  the  set  of files  originally
  distributed  by the  authors  (David Turner,  Robert Wilhelm,  and
  Werner Lemberg) as the `FreeType Project', be they named as alpha,
  beta or final release.

  `You' refers to  the licensee, or person using  the project, where
  `using' is a generic term including compiling the project's source
  code as  well as linking it  to form a  `program' or `executable'.
  This  program is  referred to  as  `a program  using the  FreeType
  engine'.

  This  license applies  to all  files distributed  in  the original
  FreeType  Project,   including  all  source   code,  binaries  and
  documentation,  unless  otherwise  stated   in  the  file  in  its
  original, unmodified form as  distributed in the original archive.
  If you are  unsure whether or not a particular  file is covered by
  this license, you must contact us to verify this.

  The FreeType  Project is copyright (C) 1996-2000  by David Turner,
  Robert Wilhelm, and Werner Lemberg.  All rights reserved except as
  specified below.

1. No Warranty
--------------

  THE FREETYPE PROJECT  IS PROVIDED `AS IS' WITHOUT  WARRANTY OF ANY
  KIND, EITHER  EXPRESS OR IMPLIED,  INCLUDING, BUT NOT  LIMITED TO,
  WARRANTIES  OF  MERCHANTABILITY   AND  FITNESS  FOR  A  PARTICULAR
  PURPOSE.  IN NO EVENT WILL ANY OF THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE  FOR ANY DAMAGES CAUSED  BY THE USE OR  THE INABILITY TO
  USE, OF THE FREETYPE PROJECT.

2. Redistribution
-----------------

  This  license  grants  a  worldwide, royalty-free,  perpetual  and
  irrevocable right  and license to use,  execute, perform, compile,
  display,  copy,   create  derivative  works   of,  distribute  and
  sublicense the  FreeType Project (in  both source and  object code
  forms)  and  derivative works  thereof  for  any  purpose; and  to
  authorize others  to exercise  some or all  of the  rights granted
  herein, subject to the following conditions:

    o Redistribution of  source code  must retain this  license file
      (`FTL.TXT') unaltered; any  additions, deletions or changes to
      the original  files must be clearly  indicated in accompanying
      documentation.   The  copyright   notices  of  the  unaltered,
      original  files must  be  preserved in  all  copies of  source
      files.

    o Redistribution in binary form must provide a  disclaimer  that
      states  that  the software is based in part of the work of the
      FreeType Team,  in  the  distribution  documentation.  We also
      encourage you to put an URL to the FreeType web page  in  your
      documentation, though this isn't mandatory.

  These conditions  apply to any  software derived from or  based on
  the FreeType Project,  not just the unmodified files.   If you use
  our work, you  must acknowledge us.  However, no  fee need be paid
  to us.

3. Advertising
--------------

  Neither the  FreeType authors and  contributors nor you  shall use
  the name of the  other for commercial, advertising, or promotional
  purposes without specific prior written permission.

  We suggest,  but do not require, that  you use one or  more of the
  following phrases to refer  to this software in your documentation
  or advertising  materials: `FreeType Project',  `FreeType Engine',
  `FreeType library', or `FreeType Distribution'.

  As  you have  not signed  this license,  you are  not  required to
  accept  it.   However,  as  the FreeType  Project  is  copyrighted
  material, only  this license, or  another one contracted  with the
  authors, grants you  the right to use, distribute,  and modify it.
  Therefore,  by  using,  distributing,  or modifying  the  FreeType
  Project, you indicate that you understand and accept all the terms
  of this license.

4. Contacts
-----------

  There are two mailing lists related to FreeType:

    o freetype@nongnu.org

      Discusses general use and applications of FreeType, as well as
      future and  wanted additions to the  library and distribution.
      If  you are looking  for support,  start in  this list  if you
      haven't found anything to help you in the documentation.

    o freetype-devel@nongnu.org

      Discusses bugs,  as well  as engine internals,  design issues,
      specific licenses, porting, etc.

  Our home page can be found at

    https://freetype.org


--- end of FTL.TXT ---
```

### licenses/system-freetype2/COPYRIGHT-NOTICE.txt

```text
/****************************************************************************
 *
 * freetype.h
 *
 *   FreeType high-level API and common types (specification only).
 *
 * Copyright (C) 1996-2026 by
 * David Turner, Robert Wilhelm, and Werner Lemberg.
 *
 * This file is part of the FreeType project, and may only be used,
 * modified, and distributed under the terms of the FreeType project
 * license, LICENSE.TXT.  By continuing to use, modify, or distribute
 * this file you indicate that you have read the license and
 * understand and accept it fully.
 *
 */
```

## libffi — 3.8.0-1.1

License: MIT

Upstream: https://sourceware.org/libffi/

### licenses/system-libffi/LICENSE

```text
libffi - Copyright (c) 1996-2026  Anthony Green, Red Hat, Inc and others.
See source files for details.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
``Software''), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ``AS IS'', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## libgcc — 16.2.1+r23+gd564253eb6c8-1

License: GPL-3.0-or-later WITH GCC Runtime Library Exception 3.1

Upstream: https://gcc.gnu.org/onlinedocs/libstdc++/manual/license.html

### licenses/system-libgcc/RUNTIME.LIBRARY.EXCEPTION

```text
GCC RUNTIME LIBRARY EXCEPTION

Version 3.1, 31 March 2009

Copyright (C) 2009 Free Software Foundation, Inc. <http://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

This GCC Runtime Library Exception ("Exception") is an additional
permission under section 7 of the GNU General Public License, version
3 ("GPLv3"). It applies to a given file (the "Runtime Library") that
bears a notice placed by the copyright holder of the file stating that
the file is governed by GPLv3 along with this Exception.

When you use GCC to compile a program, GCC may combine portions of
certain GCC header files and runtime libraries with the compiled
program. The purpose of this Exception is to allow compilation of
non-GPL (including proprietary) programs to use, in this way, the
header files and runtime libraries covered by this Exception.

0. Definitions.

A file is an "Independent Module" if it either requires the Runtime
Library for execution after a Compilation Process, or makes use of an
interface provided by the Runtime Library, but is not otherwise based
on the Runtime Library.

"GCC" means a version of the GNU Compiler Collection, with or without
modifications, governed by version 3 (or a specified later version) of
the GNU General Public License (GPL) with the option of using any
subsequent versions published by the FSF.

"GPL-compatible Software" is software whose conditions of propagation,
modification and use would permit combination with GCC in accord with
the license of GCC.

"Target Code" refers to output from any compiler for a real or virtual
target processor architecture, in executable form or suitable for
input to an assembler, loader, linker and/or execution
phase. Notwithstanding that, Target Code does not include data in any
format that is used as a compiler intermediate representation, or used
for producing a compiler intermediate representation.

The "Compilation Process" transforms code entirely represented in
non-intermediate languages designed for human-written code, and/or in
Java Virtual Machine byte code, into Target Code. Thus, for example,
use of source code generators and preprocessors need not be considered
part of the Compilation Process, since the Compilation Process can be
understood as starting with the output of the generators or
preprocessors.

A Compilation Process is "Eligible" if it is done using GCC, alone or
with other GPL-compatible software, or if it is done without using any
work based on GCC. For example, using non-GPL-compatible Software to
optimize any GCC intermediate representations would not qualify as an
Eligible Compilation Process.

1. Grant of Additional Permission.

You have permission to propagate a work of Target Code formed by
combining the Runtime Library with Independent Modules, even if such
propagation would otherwise violate the terms of GPLv3, provided that
all Target Code was generated by Eligible Compilation Processes. You
may then convey such a combination under terms of your choice,
consistent with the licensing of the Independent Modules.

2. No Weakening of GCC Copyleft.

The availability of this Exception does not imply any general
presumption that third-party software is unaffected by the copyleft
requirements of the license of GCC.
```

### licenses/system-libgcc/COPYING3

```text
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<http://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<http://www.gnu.org/philosophy/why-not-lgpl.html>.
```

### licenses/system-libgcc/COPYING.RUNTIME

```text
GCC RUNTIME LIBRARY EXCEPTION

Version 3.1, 31 March 2009

Copyright (C) 2009 Free Software Foundation, Inc. <http://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

This GCC Runtime Library Exception ("Exception") is an additional
permission under section 7 of the GNU General Public License, version
3 ("GPLv3"). It applies to a given file (the "Runtime Library") that
bears a notice placed by the copyright holder of the file stating that
the file is governed by GPLv3 along with this Exception.

When you use GCC to compile a program, GCC may combine portions of
certain GCC header files and runtime libraries with the compiled
program. The purpose of this Exception is to allow compilation of
non-GPL (including proprietary) programs to use, in this way, the
header files and runtime libraries covered by this Exception.

0. Definitions.

A file is an "Independent Module" if it either requires the Runtime
Library for execution after a Compilation Process, or makes use of an
interface provided by the Runtime Library, but is not otherwise based
on the Runtime Library.

"GCC" means a version of the GNU Compiler Collection, with or without
modifications, governed by version 3 (or a specified later version) of
the GNU General Public License (GPL) with the option of using any
subsequent versions published by the FSF.

"GPL-compatible Software" is software whose conditions of propagation,
modification and use would permit combination with GCC in accord with
the license of GCC.

"Target Code" refers to output from any compiler for a real or virtual
target processor architecture, in executable form or suitable for
input to an assembler, loader, linker and/or execution
phase. Notwithstanding that, Target Code does not include data in any
format that is used as a compiler intermediate representation, or used
for producing a compiler intermediate representation.

The "Compilation Process" transforms code entirely represented in
non-intermediate languages designed for human-written code, and/or in
Java Virtual Machine byte code, into Target Code. Thus, for example,
use of source code generators and preprocessors need not be considered
part of the Compilation Process, since the Compilation Process can be
understood as starting with the output of the generators or
preprocessors.

A Compilation Process is "Eligible" if it is done using GCC, alone or
with other GPL-compatible software, or if it is done without using any
work based on GCC. For example, using non-GPL-compatible Software to
optimize any GCC intermediate representations would not qualify as an
Eligible Compilation Process.

1. Grant of Additional Permission.

You have permission to propagate a work of Target Code formed by
combining the Runtime Library with Independent Modules, even if such
propagation would otherwise violate the terms of GPLv3, provided that
all Target Code was generated by Eligible Compilation Processes. You
may then convey such a combination under terms of your choice,
consistent with the licensing of the Independent Modules.

2. No Weakening of GCC Copyleft.

The availability of this Exception does not imply any general
presumption that third-party software is unaffected by the copyleft
requirements of the license of GCC.
```

## libpng — 1.6.59-1.1

License: libpng-2.0

Upstream: http://www.libpng.org/pub/png/libpng.html

### licenses/system-libpng/LICENSE

```text
COPYRIGHT NOTICE, DISCLAIMER, and LICENSE
=========================================

PNG Reference Library License version 2
---------------------------------------

 * Copyright (c) 1995-2026 The PNG Reference Library Authors.
 * Copyright (c) 2018-2026 Cosmin Truta.
 * Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.
 * Copyright (c) 1996-1997 Andreas Dilger.
 * Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc.

The software is supplied "as is", without warranty of any kind,
express or implied, including, without limitation, the warranties
of merchantability, fitness for a particular purpose, title, and
non-infringement.  In no event shall the Copyright owners, or
anyone distributing the software, be liable for any damages or
other liability, whether in contract, tort or otherwise, arising
from, out of, or in connection with the software, or the use or
other dealings in the software, even if advised of the possibility
of such damage.

Permission is hereby granted to use, copy, modify, and distribute
this software, or portions hereof, for any purpose, without fee,
subject to the following restrictions:

 1. The origin of this software must not be misrepresented; you
    must not claim that you wrote the original software.  If you
    use this software in a product, an acknowledgment in the product
    documentation would be appreciated, but is not required.

 2. Altered source versions must be plainly marked as such, and must
    not be misrepresented as being the original software.

 3. This Copyright notice may not be removed or altered from any
    source or altered source distribution.


PNG Reference Library License version 1 (for libpng 0.5 through 1.6.35)
-----------------------------------------------------------------------

libpng versions 1.0.7, July 1, 2000, through 1.6.35, July 15, 2018 are
Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson, are
derived from libpng-1.0.6, and are distributed according to the same
disclaimer and license as libpng-1.0.6 with the following individuals
added to the list of Contributing Authors:

    Simon-Pierre Cadieux
    Eric S. Raymond
    Mans Rullgard
    Cosmin Truta
    Gilles Vollant
    James Yu
    Mandar Sahastrabuddhe
    Google Inc.
    Vadim Barkov

and with the following additions to the disclaimer:

    There is no warranty against interference with your enjoyment of
    the library or against infringement.  There is no warranty that our
    efforts or the library will fulfill any of your particular purposes
    or needs.  This library is provided with all faults, and the entire
    risk of satisfactory quality, performance, accuracy, and effort is
    with the user.

Some files in the "contrib" directory and some configure-generated
files that are distributed with libpng have other copyright owners, and
are released under other open source licenses.

libpng versions 0.97, January 1998, through 1.0.6, March 20, 2000, are
Copyright (c) 1998-2000 Glenn Randers-Pehrson, are derived from
libpng-0.96, and are distributed according to the same disclaimer and
license as libpng-0.96, with the following individuals added to the
list of Contributing Authors:

    Tom Lane
    Glenn Randers-Pehrson
    Willem van Schaik

libpng versions 0.89, June 1996, through 0.96, May 1997, are
Copyright (c) 1996-1997 Andreas Dilger, are derived from libpng-0.88,
and are distributed according to the same disclaimer and license as
libpng-0.88, with the following individuals added to the list of
Contributing Authors:

    John Bowler
    Kevin Bracey
    Sam Bushell
    Magnus Holmgren
    Greg Roelofs
    Tom Tanner

Some files in the "scripts" directory have other copyright owners,
but are released under this license.

libpng versions 0.5, May 1995, through 0.88, January 1996, are
Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc.

For the purposes of this copyright and license, "Contributing Authors"
is defined as the following set of individuals:

    Andreas Dilger
    Dave Martindale
    Guy Eric Schalnat
    Paul Schmidt
    Tim Wegner

The PNG Reference Library is supplied "AS IS".  The Contributing
Authors and Group 42, Inc. disclaim all warranties, expressed or
implied, including, without limitation, the warranties of
merchantability and of fitness for any purpose.  The Contributing
Authors and Group 42, Inc. assume no liability for direct, indirect,
incidental, special, exemplary, or consequential damages, which may
result from the use of the PNG Reference Library, even if advised of
the possibility of such damage.

Permission is hereby granted to use, copy, modify, and distribute this
source code, or portions hereof, for any purpose, without fee, subject
to the following restrictions:

 1. The origin of this source code must not be misrepresented.

 2. Altered versions must be plainly marked as such and must not
    be misrepresented as being the original source.

 3. This Copyright notice may not be removed or altered from any
    source or altered source distribution.

The Contributing Authors and Group 42, Inc. specifically permit,
without fee, and encourage the use of this source code as a component
to supporting the PNG file format in commercial products.  If you use
this source code in a product, acknowledgment is not required but would
be appreciated.
```

## libstdc++ — 16.2.1+r23+gd564253eb6c8-1

License: GPL-3.0-or-later WITH GCC Runtime Library Exception 3.1

Upstream: https://gcc.gnu.org/onlinedocs/libstdc++/manual/license.html

### licenses/system-libstdc++/RUNTIME.LIBRARY.EXCEPTION

```text
GCC RUNTIME LIBRARY EXCEPTION

Version 3.1, 31 March 2009

Copyright (C) 2009 Free Software Foundation, Inc. <http://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

This GCC Runtime Library Exception ("Exception") is an additional
permission under section 7 of the GNU General Public License, version
3 ("GPLv3"). It applies to a given file (the "Runtime Library") that
bears a notice placed by the copyright holder of the file stating that
the file is governed by GPLv3 along with this Exception.

When you use GCC to compile a program, GCC may combine portions of
certain GCC header files and runtime libraries with the compiled
program. The purpose of this Exception is to allow compilation of
non-GPL (including proprietary) programs to use, in this way, the
header files and runtime libraries covered by this Exception.

0. Definitions.

A file is an "Independent Module" if it either requires the Runtime
Library for execution after a Compilation Process, or makes use of an
interface provided by the Runtime Library, but is not otherwise based
on the Runtime Library.

"GCC" means a version of the GNU Compiler Collection, with or without
modifications, governed by version 3 (or a specified later version) of
the GNU General Public License (GPL) with the option of using any
subsequent versions published by the FSF.

"GPL-compatible Software" is software whose conditions of propagation,
modification and use would permit combination with GCC in accord with
the license of GCC.

"Target Code" refers to output from any compiler for a real or virtual
target processor architecture, in executable form or suitable for
input to an assembler, loader, linker and/or execution
phase. Notwithstanding that, Target Code does not include data in any
format that is used as a compiler intermediate representation, or used
for producing a compiler intermediate representation.

The "Compilation Process" transforms code entirely represented in
non-intermediate languages designed for human-written code, and/or in
Java Virtual Machine byte code, into Target Code. Thus, for example,
use of source code generators and preprocessors need not be considered
part of the Compilation Process, since the Compilation Process can be
understood as starting with the output of the generators or
preprocessors.

A Compilation Process is "Eligible" if it is done using GCC, alone or
with other GPL-compatible software, or if it is done without using any
work based on GCC. For example, using non-GPL-compatible Software to
optimize any GCC intermediate representations would not qualify as an
Eligible Compilation Process.

1. Grant of Additional Permission.

You have permission to propagate a work of Target Code formed by
combining the Runtime Library with Independent Modules, even if such
propagation would otherwise violate the terms of GPLv3, provided that
all Target Code was generated by Eligible Compilation Processes. You
may then convey such a combination under terms of your choice,
consistent with the licensing of the Independent Modules.

2. No Weakening of GCC Copyleft.

The availability of this Exception does not imply any general
presumption that third-party software is unaffected by the copyleft
requirements of the license of GCC.
```

### licenses/system-libstdc++/COPYING3

```text
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<http://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<http://www.gnu.org/philosophy/why-not-lgpl.html>.
```

### licenses/system-libstdc++/COPYING.RUNTIME

```text
GCC RUNTIME LIBRARY EXCEPTION

Version 3.1, 31 March 2009

Copyright (C) 2009 Free Software Foundation, Inc. <http://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

This GCC Runtime Library Exception ("Exception") is an additional
permission under section 7 of the GNU General Public License, version
3 ("GPLv3"). It applies to a given file (the "Runtime Library") that
bears a notice placed by the copyright holder of the file stating that
the file is governed by GPLv3 along with this Exception.

When you use GCC to compile a program, GCC may combine portions of
certain GCC header files and runtime libraries with the compiled
program. The purpose of this Exception is to allow compilation of
non-GPL (including proprietary) programs to use, in this way, the
header files and runtime libraries covered by this Exception.

0. Definitions.

A file is an "Independent Module" if it either requires the Runtime
Library for execution after a Compilation Process, or makes use of an
interface provided by the Runtime Library, but is not otherwise based
on the Runtime Library.

"GCC" means a version of the GNU Compiler Collection, with or without
modifications, governed by version 3 (or a specified later version) of
the GNU General Public License (GPL) with the option of using any
subsequent versions published by the FSF.

"GPL-compatible Software" is software whose conditions of propagation,
modification and use would permit combination with GCC in accord with
the license of GCC.

"Target Code" refers to output from any compiler for a real or virtual
target processor architecture, in executable form or suitable for
input to an assembler, loader, linker and/or execution
phase. Notwithstanding that, Target Code does not include data in any
format that is used as a compiler intermediate representation, or used
for producing a compiler intermediate representation.

The "Compilation Process" transforms code entirely represented in
non-intermediate languages designed for human-written code, and/or in
Java Virtual Machine byte code, into Target Code. Thus, for example,
use of source code generators and preprocessors need not be considered
part of the Compilation Process, since the Compilation Process can be
understood as starting with the output of the generators or
preprocessors.

A Compilation Process is "Eligible" if it is done using GCC, alone or
with other GPL-compatible software, or if it is done without using any
work based on GCC. For example, using non-GPL-compatible Software to
optimize any GCC intermediate representations would not qualify as an
Eligible Compilation Process.

1. Grant of Additional Permission.

You have permission to propagate a work of Target Code formed by
combining the Runtime Library with Independent Modules, even if such
propagation would otherwise violate the terms of GPLv3, provided that
all Target Code was generated by Eligible Compilation Processes. You
may then convey such a combination under terms of your choice,
consistent with the licensing of the Independent Modules.

2. No Weakening of GCC Copyleft.

The availability of this Exception does not imply any general
presumption that third-party software is unaffected by the copyleft
requirements of the license of GCC.
```

## libx11 — 1.8.14-1.1

License: MIT AND X11

Upstream: https://gitlab.freedesktop.org/xorg/lib/libx11

### licenses/system-libx11/COPYING

```text
The following is the 'standard copyright' agreed upon by most contributors,
and is currently the canonical license preferred by the X.Org Foundation.
This is a slight variant of the common MIT license form published by the
Open Source Initiative at http://www.opensource.org/licenses/mit-license.php

Copyright holders of new code should use this license statement where
possible, and insert their name to this list.  Please sort by surname
for people, and by the full name for other entities (e.g.  Juliusz
Chroboczek sorts before Intel Corporation sorts before Daniel Stone).

See each individual source file or directory for the license that applies
to that file.

Copyright (C) 2003-2006,2008 Jamey Sharp, Josh Triplett
Copyright © 2009 Red Hat, Inc.
Copyright (c) 1990-1992, 1999, 2000, 2004, 2009, 2010, 2015, 2017, Oracle and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

 ----------------------------------------------------------------------

The following licenses are 'legacy' - usually MIT/X11 licenses with the name
of the copyright holder(s) in the license statement:

Copyright 1984-1994, 1998 The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.

X Window System is a trademark of The Open Group.

		----------------------------------------

Copyright 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1994, 1996 X Consortium
Copyright 2000 The XFree86 Project, Inc.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the X Consortium shall
not be used in advertising or otherwise to promote the sale, use or
other dealings in this Software without prior written authorization
from the X Consortium.

Copyright 1985, 1986, 1987, 1988, 1989, 1990, 1991 by
Digital Equipment Corporation

Portions Copyright 1990, 1991 by Tektronix, Inc.

Permission to use, copy, modify and distribute this documentation for
any purpose and without fee is hereby granted, provided that the above
copyright notice appears in all copies and that both that copyright notice
and this permission notice appear in all copies, and that the names of
Digital and Tektronix not be used in in advertising or publicity pertaining
to this documentation without specific, written prior permission.
Digital and Tektronix makes no representations about the suitability
of this documentation for any purpose.
It is provided ``as is'' without express or implied warranty.

		----------------------------------------

Copyright (c) 1999-2000  Free Software Foundation, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
FREE SOFTWARE FOUNDATION BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the Free Software Foundation
shall not be used in advertising or otherwise to promote the sale, use or
other dealings in this Software without prior written authorization from the
Free Software Foundation.

		----------------------------------------

Code and supporting documentation (c) Copyright 1990 1991 Tektronix, Inc.
	All Rights Reserved

This file is a component of an X Window System-specific implementation
of Xcms based on the TekColor Color Management System.  TekColor is a
trademark of Tektronix, Inc.  The term "TekHVC" designates a particular
color space that is the subject of U.S. Patent No. 4,985,853 (equivalent
foreign patents pending).  Permission is hereby granted to use, copy,
modify, sell, and otherwise distribute this software and its
documentation for any purpose and without fee, provided that:

1. This copyright, permission, and disclaimer notice is reproduced in
   all copies of this software and any modification thereof and in
   supporting documentation;
2. Any color-handling application which displays TekHVC color
   cooordinates identifies these as TekHVC color coordinates in any
   interface that displays these coordinates and in any associated
   documentation;
3. The term "TekHVC" is always used, and is only used, in association
   with the mathematical derivations of the TekHVC Color Space,
   including those provided in this file and any equivalent pathways and
   mathematical derivations, regardless of digital (e.g., floating point
   or integer) representation.

Tektronix makes no representation about the suitability of this software
for any purpose.  It is provided "as is" and with all faults.

TEKTRONIX DISCLAIMS ALL WARRANTIES APPLICABLE TO THIS SOFTWARE,
INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  IN NO EVENT SHALL TEKTRONIX BE LIABLE FOR ANY
SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
RESULTING FROM LOSS OF USE, DATA, OR PROFITS, WHETHER IN AN ACTION OF
CONTRACT, NEGLIGENCE, OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR THE PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

(c) Copyright 1995 FUJITSU LIMITED
This is source code modified by FUJITSU LIMITED under the Joint
Development Agreement for the CDE/Motif PST.

		----------------------------------------

Copyright 1992 by Oki Technosystems Laboratory, Inc.
Copyright 1992 by Fuji Xerox Co., Ltd.

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of Oki Technosystems
Laboratory and Fuji Xerox not be used in advertising or publicity
pertaining to distribution of the software without specific, written
prior permission.
Oki Technosystems Laboratory and Fuji Xerox make no representations
about the suitability of this software for any purpose.  It is provided
"as is" without express or implied warranty.

OKI TECHNOSYSTEMS LABORATORY AND FUJI XEROX DISCLAIM ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL OKI TECHNOSYSTEMS
LABORATORY AND FUJI XEROX BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1990, 1991, 1992, 1993, 1994 by FUJITSU LIMITED

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of FUJITSU LIMITED
not be used in advertising or publicity pertaining to distribution
of the software without specific, written prior permission.
FUJITSU LIMITED makes no representations about the suitability of
this software for any purpose.
It is provided "as is" without express or implied warranty.

FUJITSU LIMITED DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL FUJITSU LIMITED BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1990, 1991 by OMRON Corporation

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name OMRON not be used in
advertising or publicity pertaining to distribution of the software without
specific, written prior permission.  OMRON makes no representations
about the suitability of this software for any purpose.  It is provided
"as is" without express or implied warranty.

OMRON DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL OMRON BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTUOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1985, 1986, 1987, 1988, 1989, 1990, 1991 by
Digital Equipment Corporation

Portions Copyright 1990, 1991 by Tektronix, Inc

Rewritten for X.org by Chris Lee <clee@freedesktop.org>

Permission to use, copy, modify, distribute, and sell this documentation
for any purpose and without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
Chris Lee makes no representations about the suitability for any purpose
of the information in this document.  It is provided \`\`as-is'' without
express or implied warranty.

		----------------------------------------

Copyright 1993 by Digital Equipment Corporation, Maynard, Massachusetts,
Copyright 1994 by FUJITSU LIMITED
Copyright 1994 by Sony Corporation

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of Digital, FUJITSU
LIMITED and Sony Corporation not be used in advertising or publicity
pertaining to distribution of the software without specific, written
prior permission.

DIGITAL, FUJITSU LIMITED AND SONY CORPORATION DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL DIGITAL, FUJITSU LIMITED
AND SONY CORPORATION BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------


Copyright 1991 by the Open Software Foundation

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of Open Software Foundation
not be used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.  Open Software
Foundation makes no representations about the suitability of this
software for any purpose.  It is provided "as is" without express or
implied warranty.

OPEN SOFTWARE FOUNDATION DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL OPEN SOFTWARE FOUNDATIONN BE
LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1990, 1991, 1992,1993, 1994 by FUJITSU LIMITED
Copyright 1993, 1994                  by Sony Corporation

Permission to use, copy, modify, distribute, and sell this software and
its documentation for any purpose is hereby granted without fee, provided
that the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of FUJITSU LIMITED and Sony Corporation
not be used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.  FUJITSU LIMITED and
Sony Corporation makes no representations about the suitability of this
software for any purpose.  It is provided "as is" without express or
implied warranty.

FUJITSU LIMITED AND SONY CORPORATION DISCLAIMS ALL WARRANTIES WITH REGARD
TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL FUJITSU LIMITED OR SONY CORPORATION BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE
USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright (c) 1993, 1995 by Silicon Graphics Computer Systems, Inc.

Permission to use, copy, modify, and distribute this
software and its documentation for any purpose and without
fee is hereby granted, provided that the above copyright
notice appear in all copies and that both that copyright
notice and this permission notice appear in supporting
documentation, and that the name of Silicon Graphics not be
used in advertising or publicity pertaining to distribution
of the software without specific prior written permission.
Silicon Graphics makes no representation about the suitability
of this software for any purpose. It is provided "as is"
without any express or implied warranty.

SILICON GRAPHICS DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL SILICON
GRAPHICS BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION  WITH
THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1991, 1992, 1993, 1994 by FUJITSU LIMITED
Copyright 1993 by Digital Equipment Corporation

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of FUJITSU LIMITED and
Digital Equipment Corporation not be used in advertising or publicity
pertaining to distribution of the software without specific, written
prior permission.  FUJITSU LIMITED and Digital Equipment Corporation
makes no representations about the suitability of this software for
any purpose.  It is provided "as is" without express or implied
warranty.

FUJITSU LIMITED AND DIGITAL EQUIPMENT CORPORATION DISCLAIM ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
FUJITSU LIMITED AND DIGITAL EQUIPMENT CORPORATION BE LIABLE FOR
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.

		----------------------------------------

Copyright 1992, 1993 by FUJITSU LIMITED
Copyright 1993 by Fujitsu Open Systems Solutions, Inc.
Copyright 1994 by Sony Corporation

Permission to use, copy, modify, distribute and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of FUJITSU LIMITED,
Fujitsu Open Systems Solutions, Inc. and Sony Corporation  not be
used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.
FUJITSU LIMITED, Fujitsu Open Systems Solutions, Inc. and
Sony Corporation make no representations about the suitability of
this software for any purpose.  It is provided "as is" without
express or implied warranty.

FUJITSU LIMITED, FUJITSU OPEN SYSTEMS SOLUTIONS, INC. AND SONY
CORPORATION DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS,
IN NO EVENT SHALL FUJITSU OPEN SYSTEMS SOLUTIONS, INC., FUJITSU LIMITED
AND SONY CORPORATION BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1987, 1988, 1990, 1993 by Digital Equipment Corporation,
Maynard, Massachusetts,

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Digital not be
used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

DIGITAL DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
DIGITAL BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
SOFTWARE.

		----------------------------------------

Copyright 1993 by SunSoft, Inc.
Copyright 1999-2000 by Bruno Haible

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the names of SunSoft, Inc. and
Bruno Haible not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.  SunSoft, Inc. and Bruno Haible make no representations
about the suitability of this software for any purpose.  It is
provided "as is" without express or implied warranty.

SunSoft Inc. AND Bruno Haible DISCLAIM ALL WARRANTIES WITH REGARD
TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS, IN NO EVENT SHALL SunSoft, Inc. OR Bruno Haible BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1991 by the Open Software Foundation
Copyright 1993 by the TOSHIBA Corp.

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the names of Open Software Foundation and TOSHIBA
not be used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.  Open Software
Foundation and TOSHIBA make no representations about the suitability of this
software for any purpose.  It is provided "as is" without express or
implied warranty.

OPEN SOFTWARE FOUNDATION AND TOSHIBA DISCLAIM ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL OPEN SOFTWARE FOUNDATIONN OR TOSHIBA BE
LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1988 by Wyse Technology, Inc., San Jose, Ca.,

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name Wyse not be
used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

WYSE DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
DIGITAL BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
SOFTWARE.

		----------------------------------------


Copyright 1991 by the Open Software Foundation
Copyright 1993, 1994 by the Sony Corporation

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the names of Open Software Foundation and
Sony Corporation not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.
Open Software Foundation and Sony Corporation make no
representations about the suitability of this software for any purpose.
It is provided "as is" without express or implied warranty.

OPEN SOFTWARE FOUNDATION AND SONY CORPORATION DISCLAIM ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL OPEN
SOFTWARE FOUNDATIONN OR SONY CORPORATION BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1992, 1993 by FUJITSU LIMITED
Copyright 1993 by Fujitsu Open Systems Solutions, Inc.

Permission to use, copy, modify, distribute and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of FUJITSU LIMITED and
Fujitsu Open Systems Solutions, Inc. not be used in advertising or
publicity pertaining to distribution of the software without specific,
written prior permission.
FUJITSU LIMITED and Fujitsu Open Systems Solutions, Inc. makes no
representations about the suitability of this software for any purpose.
It is provided "as is" without express or implied warranty.

FUJITSU LIMITED AND FUJITSU OPEN SYSTEMS SOLUTIONS, INC. DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL FUJITSU OPEN SYSTEMS
SOLUTIONS, INC. AND FUJITSU LIMITED BE LIABLE FOR ANY SPECIAL, INDIRECT
OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.

		----------------------------------------

Copyright 1993, 1994 by Sony Corporation

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of Sony Corporation
not be used in advertising or publicity pertaining to distribution
of the software without specific, written prior permission.
Sony Corporation makes no representations about the suitability of
this software for any purpose. It is provided "as is" without
express or implied warranty.

SONY CORPORATION DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL SONY CORPORATION BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1986, 1998  The Open Group
Copyright (c) 2000  The XFree86 Project, Inc.

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
X CONSORTIUM OR THE XFREE86 PROJECT BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Except as contained in this notice, the name of the X Consortium or of the
XFree86 Project shall not be used in advertising or otherwise to promote the
sale, use or other dealings in this Software without prior written
authorization from the X Consortium and the XFree86 Project.

		----------------------------------------

Copyright 1990, 1991 by OMRON Corporation, NTT Software Corporation,
                     and Nippon Telegraph and Telephone Corporation
Copyright 1991 by the Open Software Foundation
Copyright 1993 by the FUJITSU LIMITED

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the names of OMRON, NTT Software, NTT, and
Open Software Foundation not be used in advertising or publicity
pertaining to distribution of the software without specific,
written prior permission. OMRON, NTT Software, NTT, and Open Software
Foundation make no representations about the suitability of this
software for any purpose.  It is provided "as is" without express or
implied warranty.

OMRON, NTT SOFTWARE, NTT, AND OPEN SOFTWARE FOUNDATION
DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
SHALL OMRON, NTT SOFTWARE, NTT, OR OPEN SOFTWARE FOUNDATION BE
LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 1988 by Wyse Technology, Inc., San Jose, Ca,
Copyright 1987 by Digital Equipment Corporation, Maynard, Massachusetts,

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name Digital not be
used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

DIGITAL AND WYSE DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL DIGITAL OR WYSE BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------


Copyright 1991, 1992 by Fuji Xerox Co., Ltd.
Copyright 1992, 1993, 1994 by FUJITSU LIMITED

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of Fuji Xerox,
FUJITSU LIMITED not be used in advertising or publicity pertaining
to distribution of the software without specific, written prior
permission. Fuji Xerox, FUJITSU LIMITED make no representations
about the suitability of this software for any purpose.
It is provided "as is" without express or implied warranty.

FUJI XEROX, FUJITSU LIMITED DISCLAIM ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL FUJI XEROX,
FUJITSU LIMITED BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 2006 Josh Triplett

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

		----------------------------------------

Copyright 1990, 1991 by OMRON Corporation, NTT Software Corporation,
                     and Nippon Telegraph and Telephone Corporation
Copyright 1991 by the Open Software Foundation
Copyright 1993 by the TOSHIBA Corp.
Copyright 1993, 1994 by Sony Corporation
Copyright 1993, 1994 by the FUJITSU LIMITED

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the names of OMRON, NTT Software, NTT, Open
Software Foundation, and Sony Corporation not be used in advertising
or publicity pertaining to distribution of the software without specific,
written prior permission. OMRON, NTT Software, NTT, Open Software
Foundation, and Sony Corporation  make no representations about the
suitability of this software for any purpose.  It is provided "as is"
without express or implied warranty.

OMRON, NTT SOFTWARE, NTT, OPEN SOFTWARE FOUNDATION, AND SONY
CORPORATION DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
SHALL OMRON, NTT SOFTWARE, NTT, OPEN SOFTWARE FOUNDATION, OR SONY
CORPORATION BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright 2000 by Bruno Haible

Permission to use, copy, modify, distribute, and sell this software
and its documentation for any purpose is hereby granted without fee,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the name of Bruno Haible not
be used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.  Bruno Haible
makes no representations about the suitability of this software for
any purpose.  It is provided "as is" without express or implied
warranty.

Bruno Haible DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
NO EVENT SHALL Bruno Haible BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright © 2003 Keith Packard

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of Keith Packard not be used in
advertising or publicity pertaining to distribution of the software without
specific, written prior permission.  Keith Packard makes no
representations about the suitability of this software for any purpose.  It
is provided "as is" without express or implied warranty.

KEITH PACKARD DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL KEITH PACKARD BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright (c) 2007-2009, Troy D. Hanson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

		----------------------------------------

Copyright 1992, 1993 by TOSHIBA Corp.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted, provided
that the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of TOSHIBA not be used in advertising
or publicity pertaining to distribution of the software without specific,
written prior permission. TOSHIBA make no representations about the
suitability of this software for any purpose.  It is provided "as is"
without express or implied warranty.

TOSHIBA DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
TOSHIBA BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
SOFTWARE.


		----------------------------------------

Copyright IBM Corporation 1993

All Rights Reserved

License to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of IBM not be
used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

IBM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS, AND
NONINFRINGEMENT OF THIRD PARTY RIGHTS, IN NO EVENT SHALL
IBM BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
SOFTWARE.

		----------------------------------------

Copyright 1990, 1991 by OMRON Corporation, NTT Software Corporation,
                     and Nippon Telegraph and Telephone Corporation

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the names of OMRON, NTT Software, and NTT
not be used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission. OMRON, NTT Software,
and NTT make no representations about the suitability of this
software for any purpose.  It is provided "as is" without express or
implied warranty.

OMRON, NTT SOFTWARE, AND NTT, DISCLAIM ALL WARRANTIES WITH REGARD
TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS, IN NO EVENT SHALL OMRON, NTT SOFTWARE, OR NTT, BE
LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

		----------------------------------------

Copyright (c) 2008 Otto Moerbeek <otto@drijf.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## libxau — 1.0.12-1.1

License: MIT-open-group

Upstream: https://xorg.freedesktop.org/

### licenses/system-libxau/COPYING

```text
Copyright 1988, 1993, 1994, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.
```

## libxdmcp — 1.1.5-2.1

License: MIT-open-group

Upstream: https://gitlab.freedesktop.org/xorg/lib/libxdmcp

### licenses/system-libxdmcp/COPYING

```text
Copyright 1989, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.

Author:  Keith Packard, MIT X Consortium
```

## libxext — 1.3.7-1.1

License: LicenseRef-libxext

Upstream: https://gitlab.freedesktop.org/xorg/lib/libxext

### licenses/system-libxext/COPYING

```text
Copyright 1986, 1987, 1988, 1989, 1994, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.

Copyright (c) 1996 Digital Equipment Corporation, Maynard, Massachusetts.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
DIGITAL EQUIPMENT CORPORATION BE LIABLE FOR ANY CLAIM, DAMAGES, INCLUDING,
BUT NOT LIMITED TO CONSEQUENTIAL OR INCIDENTAL DAMAGES, OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of Digital Equipment Corporation
shall not be used in advertising or otherwise to promote the sale, use or other
dealings in this Software without prior written authorization from Digital
Equipment Corporation.

Copyright (c) 1997 by Silicon Graphics Computer Systems, Inc.
Permission to use, copy, modify, and distribute this
software and its documentation for any purpose and without
fee is hereby granted, provided that the above copyright
notice appear in all copies and that both that copyright
notice and this permission notice appear in supporting
documentation, and that the name of Silicon Graphics not be
used in advertising or publicity pertaining to distribution
of the software without specific prior written permission.
Silicon Graphics makes no representation about the suitability
of this software for any purpose. It is provided "as is"
without any express or implied warranty.
SILICON GRAPHICS DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL SILICON
GRAPHICS BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION  WITH
THE USE OR PERFORMANCE OF THIS SOFTWARE.

Copyright 1992 Network Computing Devices

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of NCD. not be used in advertising or
publicity pertaining to distribution of the software without specific,
written prior permission.  NCD. makes no representations about the
suitability of this software for any purpose.  It is provided "as is"
without express or implied warranty.

NCD. DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL NCD.
BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Copyright 1991,1993 by Digital Equipment Corporation, Maynard, Massachusetts,
and Olivetti Research Limited, Cambridge, England.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of Digital or Olivetti
not be used in advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

DIGITAL AND OLIVETTI DISCLAIM ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THEY BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

Copyright 1986, 1987, 1988 by Hewlett-Packard Corporation

Permission to use, copy, modify, and distribute this
software and its documentation for any purpose and without
fee is hereby granted, provided that the above copyright
notice appear in all copies and that both that copyright
notice and this permission notice appear in supporting
documentation, and that the name of Hewlett-Packard not be used in
advertising or publicity pertaining to distribution of the
software without specific, written prior permission.

Hewlett-Packard makes no representations about the
suitability of this software for any purpose.  It is provided
"as is" without express or implied warranty.

This software is not subject to any license of the American
Telephone and Telegraph Company or of the Regents of the
University of California.

Copyright (c) 1994, 1995  Hewlett-Packard Company

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL HEWLETT-PACKARD COMPANY BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the Hewlett-Packard
Company shall not be used in advertising or otherwise to promote the
sale, use or other dealings in this Software without prior written
authorization from the Hewlett-Packard Company.

Copyright Digital Equipment Corporation, 1996

Permission to use, copy, modify, distribute, and sell this
documentation for any purpose is hereby granted without fee,
provided that the above copyright notice and this permission
notice appear in all copies.  Digital Equipment Corporation
makes no representations about the suitability for any purpose
of the information in this document.  This documentation is
provided ``as is'' without express or implied warranty.

Copyright (c) 1999, 2005, 2006, 2013, 2015, Oracle and/or its affiliates.
Copyright © 2007-2008 Peter Hutterer

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

Copyright (c) 1989 X Consortium, Inc. and Digital Equipment Corporation.
Copyright (c) 1992 X Consortium, Inc. and Intergraph Corporation.
Copyright (c) 1993 X Consortium, Inc. and Silicon Graphics, Inc.
Copyright (c) 1994, 1995 X Consortium, Inc. and Hewlett-Packard Company.

Permission to use, copy, modify, and distribute this documentation for
any purpose and without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
Digital Equipment Corporation, Intergraph Corporation, Silicon
Graphics, Hewlett-Packard, and the X Consortium make no
representations about the suitability for any purpose of the
information in this document.  This documentation is provided ``as is''
without express or implied warranty.

Copyright (c) 2008 Otto Moerbeek <otto@drijf.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## libxft — 2.3.9-1.2

License: HPND-sell-variant

Upstream: https://xorg.freedesktop.org/

### licenses/system-libxft/COPYING

```text

Copyright © 2001,2003 Keith Packard

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of Keith Packard not be used in
advertising or publicity pertaining to distribution of the software without
specific, written prior permission.  Keith Packard makes no
representations about the suitability of this software for any purpose.  It
is provided "as is" without express or implied warranty.

KEITH PACKARD DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL KEITH PACKARD BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```

## libxrender — 0.9.13-1.1

License: HPND-sell-variant

Upstream: https://xorg.freedesktop.org/

### licenses/system-libxrender/COPYING

```text

Copyright © 2001,2003 Keith Packard

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of Keith Packard not be used in
advertising or publicity pertaining to distribution of the software without
specific, written prior permission.  Keith Packard makes no
representations about the suitability of this software for any purpose.  It
is provided "as is" without express or implied warranty.

KEITH PACKARD DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL KEITH PACKARD BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

Copyright © 2000 SuSE, Inc.

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of SuSE not be used in advertising or
publicity pertaining to distribution of the software without specific,
written prior permission.  SuSE makes no representations about the
suitability of this software for any purpose.  It is provided "as is"
without express or implied warranty.

SuSE DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL SuSE
BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

## libxss — 1.2.5-1.1

License: X11

Upstream: https://gitlab.freedesktop.org/xorg/lib/libxscrnsaver

### licenses/system-libxss/COPYING

```text
Copyright (c) 1992  X Consortium

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
X CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the X Consortium shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from the X Consortium.


Copyright (C) 2003 The XFree86 Project, Inc.  All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
IN NO EVENT SHALL THE XFREE86 PROJECT BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the XFree86 Project
shall not be used in advertising or otherwise to promote the sale, use
or other dealings in this Software without prior written authorization
from the XFree86 Project.
```

## mpdecimal — 4.0.1-3.1

License: BSD-2-Clause

Upstream: https://www.bytereef.org/mpdecimal/index.html

### licenses/system-mpdecimal/COPYRIGHT.txt

```text
Copyright (c) 2008-2025 Stefan Krah. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
```

## openssl — 3.6.5-1.1

License: Apache-2.0

Upstream: https://github.com/openssl/openssl/blob/openssl-3.6.5/LICENSE.txt

### licenses/system-openssl/LICENSE.txt

```text

                                 Apache License
                           Version 2.0, January 2004
                        https://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS
```

### licenses/system-openssl/AUTHORS.md

```text
Authors
=======

This is the list of OpenSSL authors for copyright purposes.
It does not necessarily list everyone who has contributed code,
since in some cases, their employer may be the copyright holder.
To see the full list of contributors, see the revision history in
source control.

Groups
------

 * OpenSSL Software Services, Inc.
 * OpenSSL Software Foundation, Inc.
 * Google LLC

Individuals
-----------

 * Andy Polyakov
 * Ben Laurie
 * Ben Kaduk
 * Bernd Edlinger
 * Bodo Möller
 * David Benjamin
 * David von Oheimb
 * Dmitry Belyavskiy (Дмитрий Белявский)
 * Emilia Käsper
 * Eric Young
 * Geoff Thorpe
 * Holger Reif
 * Kurt Roeckx
 * Lutz Jänicke
 * Mark J. Cox
 * Matt Caswell
 * Matthias St. Pierre
 * Nicola Tuveri
 * Nils Larsch
 * Patrick Steuer
 * Paul Dale
 * Paul C. Sutton
 * Paul Yang
 * Ralf S. Engelschall
 * Rich Salz
 * Richard Levitte
 * Shane Lontis
 * Stephen Henson
 * Steve Marquess
 * Tim Hudson
 * Tomáš Mráz
 * Ulf Möller
 * Valerii Krygin
 * Viktor Dukhovni
```

### licenses/system-openssl/ACKNOWLEDGEMENTS.md

```text
Acknowledgements
================

Please see our [Thanks!][] page for the current acknowledgements.

[Thanks!]: https://www.openssl.org/community/thanks.html
```

## python — 3.14.8-1

License: PSF-2.0

Upstream: https://www.python.org/

### licenses/system-python/LICENSE.txt

```text
A. HISTORY OF THE SOFTWARE
==========================

Python was created in the early 1990s by Guido van Rossum at Stichting
Mathematisch Centrum (CWI, see https://www.cwi.nl) in the Netherlands
as a successor of a language called ABC.  Guido remains Python's
principal author, although it includes many contributions from others.

In 1995, Guido continued his work on Python at the Corporation for
National Research Initiatives (CNRI, see https://www.cnri.reston.va.us)
in Reston, Virginia where he released several versions of the
software.

In May 2000, Guido and the Python core development team moved to
BeOpen.com to form the BeOpen PythonLabs team.  In October of the same
year, the PythonLabs team moved to Digital Creations, which became
Zope Corporation.  In 2001, the Python Software Foundation (PSF, see
https://www.python.org/psf/) was formed, a non-profit organization
created specifically to own Python-related Intellectual Property.
Zope Corporation was a sponsoring member of the PSF.

All Python releases are Open Source (see https://opensource.org for
the Open Source Definition).  Historically, most, but not all, Python
releases have also been GPL-compatible; the table below summarizes
the various releases.

    Release         Derived     Year        Owner       GPL-
                    from                                compatible? (1)

    0.9.0 thru 1.2              1991-1995   CWI         yes
    1.3 thru 1.5.2  1.2         1995-1999   CNRI        yes
    1.6             1.5.2       2000        CNRI        no
    2.0             1.6         2000        BeOpen.com  no
    1.6.1           1.6         2001        CNRI        yes (2)
    2.1             2.0+1.6.1   2001        PSF         no
    2.0.1           2.0+1.6.1   2001        PSF         yes
    2.1.1           2.1+2.0.1   2001        PSF         yes
    2.1.2           2.1.1       2002        PSF         yes
    2.1.3           2.1.2       2002        PSF         yes
    2.2 and above   2.1.1       2001-now    PSF         yes

Footnotes:

(1) GPL-compatible doesn't mean that we're distributing Python under
    the GPL.  All Python licenses, unlike the GPL, let you distribute
    a modified version without making your changes open source.  The
    GPL-compatible licenses make it possible to combine Python with
    other software that is released under the GPL; the others don't.

(2) According to Richard Stallman, 1.6.1 is not GPL-compatible,
    because its license has a choice of law clause.  According to
    CNRI, however, Stallman's lawyer has told CNRI's lawyer that 1.6.1
    is "not incompatible" with the GPL.

Thanks to the many outside volunteers who have worked under Guido's
direction to make these releases possible.


B. TERMS AND CONDITIONS FOR ACCESSING OR OTHERWISE USING PYTHON
===============================================================

Python software and documentation are licensed under the
Python Software Foundation License Version 2.

Starting with Python 3.8.6, examples, recipes, and other code in
the documentation are dual licensed under the PSF License Version 2
and the Zero-Clause BSD license.

Some software incorporated into Python is under different licenses.
The licenses are listed with code falling under that license.


PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001 Python Software Foundation; All Rights Reserved"
are retained in Python alone or in any derivative version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS"
basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee.  This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.


BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
-------------------------------------------

BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1

1. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
Individual or Organization ("Licensee") accessing and otherwise using
this software in source or binary form and its associated
documentation ("the Software").

2. Subject to the terms and conditions of this BeOpen Python License
Agreement, BeOpen hereby grants Licensee a non-exclusive,
royalty-free, world-wide license to reproduce, analyze, test, perform
and/or display publicly, prepare derivative works, distribute, and
otherwise use the Software alone or in any derivative version,
provided, however, that the BeOpen Python License is retained in the
Software, alone or in any derivative version prepared by Licensee.

3. BeOpen is making the Software available to Licensee on an "AS IS"
basis.  BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

4. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR ANY
DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

5. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

6. This License Agreement shall be governed by and interpreted in all
respects by the law of the State of California, excluding conflict of
law provisions.  Nothing in this License Agreement shall be deemed to
create any relationship of agency, partnership, or joint venture
between BeOpen and Licensee.  This License Agreement does not grant
permission to use BeOpen trademarks or trade names in a trademark
sense to endorse or promote products or services of Licensee, or any
third party.  As an exception, the "BeOpen Python" logos available at
http://www.pythonlabs.com/logos.html may be used according to the
permissions granted on that web page.

7. By copying, installing or otherwise using the software, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.


CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1
---------------------------------------

1. This LICENSE AGREEMENT is between the Corporation for National
Research Initiatives, having an office at 1895 Preston White Drive,
Reston, VA 20191 ("CNRI"), and the Individual or Organization
("Licensee") accessing and otherwise using Python 1.6.1 software in
source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, CNRI
hereby grants Licensee a nonexclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display publicly,
prepare derivative works, distribute, and otherwise use Python 1.6.1
alone or in any derivative version, provided, however, that CNRI's
License Agreement and CNRI's notice of copyright, i.e., "Copyright (c)
1995-2001 Corporation for National Research Initiatives; All Rights
Reserved" are retained in Python 1.6.1 alone or in any derivative
version prepared by Licensee.  Alternately, in lieu of CNRI's License
Agreement, Licensee may substitute the following text (omitting the
quotes): "Python 1.6.1 is made available subject to the terms and
conditions in CNRI's License Agreement.  This Agreement together with
Python 1.6.1 may be located on the internet using the following
unique, persistent identifier (known as a handle): 1895.22/1013.  This
Agreement may also be obtained from a proxy server on the internet
using the following URL: http://hdl.handle.net/1895.22/1013".

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python 1.6.1 or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python 1.6.1.

4. CNRI is making Python 1.6.1 available to Licensee on an "AS IS"
basis.  CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6.1 WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
1.6.1 FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON 1.6.1,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. This License Agreement shall be governed by the federal
intellectual property law of the United States, including without
limitation the federal copyright law, and, to the extent such
U.S. federal law does not apply, by the law of the Commonwealth of
Virginia, excluding Virginia's conflict of law provisions.
Notwithstanding the foregoing, with regard to derivative works based
on Python 1.6.1 that incorporate non-separable material that was
previously distributed under the GNU General Public License (GPL), the
law of the Commonwealth of Virginia shall govern this License
Agreement only as to issues arising under or with respect to
Paragraphs 4, 5, and 7 of this License Agreement.  Nothing in this
License Agreement shall be deemed to create any relationship of
agency, partnership, or joint venture between CNRI and Licensee.  This
License Agreement does not grant permission to use CNRI trademarks or
trade name in a trademark sense to endorse or promote products or
services of Licensee, or any third party.

8. By clicking on the "ACCEPT" button where indicated, or by copying,
installing or otherwise using Python 1.6.1, Licensee agrees to be
bound by the terms and conditions of this License Agreement.

        ACCEPT


CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2
--------------------------------------------------

Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
The Netherlands.  All rights reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

ZERO-CLAUSE BSD LICENSE FOR CODE IN THE PYTHON DOCUMENTATION
----------------------------------------------------------------------

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```

## sdl2-compat — 2.32.74-1.1

License: Zlib

Upstream: https://github.com/libsdl-org/sdl2-compat

### licenses/system-sdl2-compat/LICENSE.txt

```text
Copyright (C) 2026 Sam Lantinga <slouken@libsdl.org>

This software is provided 'as-is', without any express or implied
warranty.  In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required. 
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
```

## sdl2_mixer — 2.8.2-1.1

License: Zlib (actual upstream and installed notice; package metadata says MIT)

Upstream: https://github.com/libsdl-org/SDL_mixer/blob/release-2.8.2/LICENSE.txt

### licenses/system-sdl2_mixer/LICENSE

```text
Copyright (C) 1997-2025 Sam Lantinga <slouken@libsdl.org>

This software is provided 'as-is', without any express or implied
warranty.  In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
```

## sqlite — 3.54.0-1

License: Public-domain dedication (SQLite)

Upstream: https://www.sqlite.org/copyright.html

### licenses/system-sqlite/license.txt

```text
SQLite Copyright
SQLite is in the
Public Domain 


All of the deliverable code in SQLite has been dedicated to the public domain by the authors. All code authors, and representatives of the companies they work for, have signed affidavits dedicating their contributions to the public domain and originals of those signed affidavits are stored in a firesafe at the main offices of Hwaci. Anyone is free to copy, modify, publish, use, compile, sell, or distribute the original SQLite code, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means. 

The previous paragraph applies to the deliverable code in SQLite - those parts of the SQLite library that you actually bundle and ship with a larger application. Portions of the documentation and some code used as part of the build process might fall under other licenses. The details here are unclear. We do not worry about the licensing of the documentation and build code so much because none of these things are part of the core deliverable SQLite library. 

All of the deliverable code in SQLite has been written from scratch. No code has been taken from other projects or from the open internet. Every line of code can be traced back to its original author, and all of those authors have public domain dedications on file. So the SQLite code base is clean and is uncontaminated with licensed code from other projects. 
Obtaining An Explicit License To Use SQLite

Even though SQLite is in the public domain and does not require a license, some users want to obtain a license anyway. Some reasons for obtaining a license include: 
You are using SQLite in a jurisdiction that does not recognize the public domain. 
You are using SQLite in a jurisdiction that does not recognize the right of an author to dedicate their work to the public domain. 
You want to hold a tangible legal document as evidence that you have the legal right to use and distribute SQLite. 
Your legal department tells you that you have to purchase a license. 

If you feel like you really have to purchase a license for SQLite, Hwaci, the company that employs the architect and principal developers of SQLite, will sell you one. 
Contributed Code

In order to keep SQLite completely free and unencumbered by copyright, all new contributors to the SQLite code base are asked to dedicate their contributions to the public domain. If you want to send a patch or enhancement for possible inclusion in the SQLite source tree, please accompany the patch with the following statement: 
The author or authors of this code dedicate any and all copyright interest in this code to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this code under copyright law. 

We are not able to accept patches or changes to SQLite that are not accompanied by a statement such as the above. In addition, if you make changes or enhancements as an employee, then a simple statement such as the above is insufficient. You must also send by surface mail a copyright release signed by a company officer. A signed original of the copyright release should be mailed to:
Hwaci
6200 Maple Cove Lane
Charlotte, NC 28269
USA 

A template copyright release is available in PDF or HTML. You can use this release to make future changes.

see http://www.sqlite.org/copyright.html
```

## tcl — 8.6.16-1.1

License: TCL

Upstream: http://tcl.sourceforge.net/

### licenses/system-tcl/license.terms

```text
This software is copyrighted by the Regents of the University of
California, Sun Microsystems, Inc., Scriptics Corporation, ActiveState
Corporation and other parties.  The following terms apply to all files
associated with the software unless explicitly disclaimed in
individual files.

The authors hereby grant permission to use, copy, modify, distribute,
and license this software and its documentation for any purpose, provided
that existing copyright notices are retained in all copies and that this
notice is included verbatim in any distributions. No written agreement,
license, or royalty fee is required for any of the authorized uses.
Modifications to this software may be copyrighted by their authors
and need not follow the licensing terms described here, provided that
the new terms are clearly indicated on the first page of each file where
they apply.

IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.

GOVERNMENT USE: If you are acquiring this software on behalf of the
U.S. government, the Government shall have only "Restricted Rights"
in the software and related documentation as defined in the Federal
Acquisition Regulations (FARs) in Clause 52.227.19 (c) (2).  If you
are acquiring the software on behalf of the Department of Defense, the
software shall be classified as "Commercial Computer Software" and the
Government shall have only "Restricted Rights" as defined in Clause
252.227-7014 (b) (3) of DFARs.  Notwithstanding the foregoing, the
authors grant the U.S. Government and others acting in its behalf
permission to use and distribute the software in accordance with the
terms specified in this license.
```

## tk — 8.6.16-1.1

License: TCL

Upstream: http://tcl.sourceforge.net/

### licenses/system-tk/license.terms

```text
This software is copyrighted by the Regents of the University of
California, Sun Microsystems, Inc., Scriptics Corporation, ActiveState
Corporation, Apple Inc. and other parties.  The following terms apply to
all files associated with the software unless explicitly disclaimed in
individual files.

The authors hereby grant permission to use, copy, modify, distribute,
and license this software and its documentation for any purpose, provided
that existing copyright notices are retained in all copies and that this
notice is included verbatim in any distributions. No written agreement,
license, or royalty fee is required for any of the authorized uses.
Modifications to this software may be copyrighted by their authors
and need not follow the licensing terms described here, provided that
the new terms are clearly indicated on the first page of each file where
they apply.

IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.

GOVERNMENT USE: If you are acquiring this software on behalf of the
U.S. government, the Government shall have only "Restricted Rights"
in the software and related documentation as defined in the Federal
Acquisition Regulations (FARs) in Clause 52.227.19 (c) (2).  If you
are acquiring the software on behalf of the Department of Defense, the
software shall be classified as "Commercial Computer Software" and the
Government shall have only "Restricted Rights" as defined in Clause
252.227-7013 (b) (3) of DFARs.  Notwithstanding the foregoing, the
authors grant the U.S. Government and others acting in its behalf
permission to use and distribute the software in accordance with the
terms specified in this license.
```

## util-linux-libs — 2.42.4-1.1

License: libuuid: BSD-3-Clause; not every util-linux package license applies

Upstream: https://github.com/util-linux/util-linux/blob/master/libuuid/COPYING

Only libuuid is shipped from util-linux. Its BSD-3-Clause terms are selected; GPL utilities from that source package are not included.

### licenses/system-util-linux-libs/COPYING.BSD-3-Clause

```text
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, and the entire permission notice in its entirety,
   including the disclaimer of warranties.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote
   products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
```

### licenses/system-util-linux-libs/SOURCE-NOTICES.txt

```text

clear.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/clear.c
/*
 * clear.c -- Clear a UUID
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

compare.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/compare.c
/*
 * compare.c --- compare whether or not two UUIDs are the same
 *
 * Returns 0 if the two UUIDs are different, and 1 if they are the same.
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

copy.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/copy.c
/*
 * copy.c --- copy UUIDs
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

gen_uuid.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/gen_uuid.c
/*
 * gen_uuid.c --- generate a DCE-compatible uuid
 *
 * Copyright (C) 1996, 1997, 1998, 1999 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

isnull.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/isnull.c
/*
 * isnull.c --- Check whether or not the UUID is null
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

pack.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/pack.c
/*
 * Internal routine for packing UUIDs
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

parse.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/parse.c
/*
 * parse.c --- UUID parsing
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

predefined.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/predefined.c
/*
 * predefined.c --- well-known UUIDs from the RFC-4122 namespace
 *
 * Copyright (C) 2017 Philip Prindeville
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

test_uuid.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/test_uuid.c
/*
 * tst_uuid.c --- test program from the UUID library
 *
 * Copyright (C) 1996, 1997, 1998 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

unpack.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/unpack.c
/*
 * Internal routine for unpacking UUID
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

unparse.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/unparse.c
/*
 * unparse.c -- convert a UUID to string
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

uuid.h
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/uuid.h
/*
 * Public include file for the UUID library
 *
 * Copyright (C) 1996, 1997, 1998 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

uuidP.h
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/uuidP.h
/*
 * uuid.h -- private header file for uuids
 *
 * Copyright (C) 1996, 1997 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

uuid_time.c
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/uuid_time.c
/*
 * uuid_time.c --- Interpret the time field from a uuid.  This program
 * 	violates the UUID abstraction barrier by reaching into the guts
 *	of a UUID and interpreting it.
 *
 * Copyright (C) 1998, 1999 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */

uuidd.h
Source: https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/libuuid/src/uuidd.h
/*
 * Definitions used by the uuidd daemon
 *
 * Copyright (C) 2007 Theodore Ts'o.
 *
 * %Begin-Header%
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, and the entire permission notice in its entirety,
 *    including the disclaimer of warranties.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 * %End-Header%
 */
```

## xz — 5.8.3-1

License: liblzma: 0BSD; not the entire XZ project license union

Upstream: https://github.com/tukaani-project/xz/blob/v5.8.3/COPYING

### licenses/system-xz/COPYING

```text

XZ Utils Licensing
==================

    Different licenses apply to different files in this package. Here
    is a summary of which licenses apply to which parts of this package:

      - liblzma is under the BSD Zero Clause License (0BSD).

      - The command line tools xz, xzdec, lzmadec, and lzmainfo are
        under 0BSD except that, on systems that don't have a usable
        getopt_long, GNU getopt_long is compiled and linked in from the
        'lib' directory. The getopt_long code is under GNU LGPLv2.1+.

      - The scripts to grep, diff, and view compressed files have been
        adapted from GNU gzip. These scripts (xzgrep, xzdiff, xzless,
        and xzmore) are under GNU GPLv2+. The man pages of the scripts
        are under 0BSD; they aren't based on the man pages of GNU gzip.

      - Most of the XZ Utils specific documentation that is in
        plain text files (like README, INSTALL, PACKAGERS, NEWS,
        and ChangeLog) are under 0BSD unless stated otherwise in
        the file itself. The files xz-file-format.txt and
        lzma-file-format.xt are in the public domain but may
        be distributed under the terms of 0BSD too.

      - Translated messages and man pages are under 0BSD except that
        some old translations are in the public domain.

      - Test files and test code in the 'tests' directory, and
        debugging utilities in the 'debug' directory are under
        the BSD Zero Clause License (0BSD).

      - The GNU Autotools based build system contains files that are
        under GNU GPLv2+, GNU GPLv3+, and a few permissive licenses.
        These files don't affect the licensing of the binaries being
        built.

      - The 'extra' directory contains files that are under various
        free software licenses. These aren't built or installed as
        part of XZ Utils.

    The following command may be helpful in finding per-file license
    information. It works on xz.git and on a clean file tree extracted
    from a release tarball.

        sh build-aux/license-check.sh -v

    For the files under the BSD Zero Clause License (0BSD), if
    a copyright notice is needed, the following is sufficient:

        Copyright (C) The XZ Utils authors and contributors

    If you copy significant amounts of 0BSD-licensed code from XZ Utils
    into your project, acknowledging this somewhere in your software is
    polite (especially if it is proprietary, non-free software), but
    it is not legally required by the license terms. Here is an example
    of a good notice to put into "about box" or into documentation:

        This software includes code from XZ Utils <https://tukaani.org/xz/>.

    The following license texts are included in the following files:
      - COPYING.0BSD: BSD Zero Clause License
      - COPYING.LGPLv2.1: GNU Lesser General Public License version 2.1
      - COPYING.GPLv2: GNU General Public License version 2
      - COPYING.GPLv3: GNU General Public License version 3

    If you have questions, don't hesitate to ask for more information.
    The contact information is in the README file.
```

## zlib-ng-compat — 2.3.3-2

License: Zlib

Upstream: https://github.com/zlib-ng/zlib-ng

### licenses/system-zlib-ng-compat/LICENSE.md

```text
(C) 1995-2024 Jean-loup Gailly and Mark Adler

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

3. This notice may not be removed or altered from any source distribution.
```

## zstd — 1.5.7-4

License: BSD-3-Clause (selected alternative to GPL)

Upstream: https://github.com/facebook/zstd/blob/v1.5.7/LICENSE

### licenses/system-zstd/LICENSE

```text
BSD License

For Zstandard software

Copyright (c) Meta Platforms, Inc. and affiliates. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

 * Neither the name Facebook, nor Meta, nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

