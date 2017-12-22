/*
 * Copyright (c) 2016, Intel Corporation
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   * Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   * Neither the name of Intel Corporation nor the names of its contributors
 *     may be used to endorse or promote products derived from this software
 *     without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef UID_H_
#define	UID_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdio.h>
#include <common_types.h>

NVM_COMMON_API extern void uid_copy(const char *src, COMMON_UID dst);

NVM_COMMON_API extern void guid_to_uid(const COMMON_GUID guid, COMMON_UID uid);

NVM_COMMON_API extern int uid_cmp(const COMMON_UID uid1, const COMMON_UID uid2);
NVM_COMMON_API extern int get_uid_index(const COMMON_UID uid, const COMMON_UID *uid_list,
		const COMMON_UINT16 uid_list_len);
NVM_COMMON_API extern COMMON_BOOL is_uid_in_list(const COMMON_UID uid, const COMMON_UID *uid_list,
		const COMMON_UINT16 uid_list_len);

#ifdef __cplusplus
}
#endif

#endif /* UID_H_ */
