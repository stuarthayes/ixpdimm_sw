/*
 * Copyright (c) 2015 2016, Intel Corporation
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

/*
 * This file defines the smart caching interface
 */

#ifndef	_NVM_CONTEXT_H_
#define	_NVM_CONTEXT_H_

#include "nvm_management.h"
#include "adapter_types.h"
#include <acpi/nfit_tables.h>
#include "export_api.h"

#ifdef __cplusplus
extern "C"
{
#endif

/*
 * The context of an NVM-DIMM
 */
struct nvm_device_context
{
	NVM_UID uid;
	struct device_discovery *p_device_discovery;
	struct device_details *p_device_details;
	NVM_SIZE pcd_size;
	struct platform_config_data *p_pcd;
};

/*
 * The context of an namespace
 */
struct nvm_namespace_context
{
	NVM_UID uid;
	struct namespace_discovery *p_namespace_discovery;
	struct namespace_details *p_namespace_details;
};

/*
 * Overall system context
 */
struct nvm_context
{
	struct nvm_capabilities *p_capabilities;
	int device_count;
	struct nvm_device_context *p_devices;
	int pool_count;
	struct pool *p_pools;
	int namespace_count;
	struct nvm_namespace_context *p_namespaces;

	// avoid unnecessary calls to the read PCD
	int pcd_namespace_count;
	struct nvm_namespace_details *p_pcd_namespaces;

	// avoid unnecessary calls to retrieve ACPI tables
	int nfit_size;
	struct parsed_nfit *p_nfit;
};

NVM_API extern struct nvm_context *p_context;

// capabilities
NVM_API int get_nvm_context_capabilities(struct nvm_capabilities *p_capabilities);
NVM_API int set_nvm_context_capabilities(const struct nvm_capabilities *p_capabilities);

// devices
NVM_API void invalidate_devices();
NVM_API void invalidate_device_pcd(const NVM_UID device_uid);
NVM_API int get_nvm_context_device_count();
NVM_API int get_nvm_context_devices(struct device_discovery *p_devices, const int dev_count);
NVM_API int set_nvm_context_devices(const struct device_discovery *p_devices, const int dev_count);
NVM_API int get_nvm_context_device_details(const NVM_UID device_uid,
		struct device_details *p_details);
NVM_API int set_nvm_context_device_details(const NVM_UID device_uid,
		const struct device_details *p_details);
NVM_API int get_nvm_context_device_pcd(const NVM_UID device_uid,
		struct platform_config_data **pp_pcd, NVM_SIZE *p_pcd_size);
NVM_API int set_nvm_context_device_pcd(const NVM_UID device_uid,
		const struct platform_config_data *p_pcd, const NVM_SIZE pcd_size);

// pools
NVM_API void invalidate_pools();
NVM_API int get_nvm_context_pool_count();
NVM_API int get_nvm_context_pools(struct pool *p_pools, const int pool_count);
NVM_API int set_nvm_context_pools(const struct pool *p_pools, const int pool_count);
NVM_API int get_nvm_context_pool(const NVM_UID pool_uid, struct pool *p_pool);

// namespaces
NVM_API void invalidate_namespaces();
NVM_API int get_nvm_context_namespace_count();
NVM_API int get_nvm_context_namespaces(struct namespace_discovery *p_namespaces,
		const int namespace_count);
NVM_API int set_nvm_context_namespaces(const struct namespace_discovery *p_namespaces,
		const int namespace_count);
NVM_API int get_nvm_context_namespace_details(const NVM_UID namespace_uid,
		struct namespace_details *p_namespace);
NVM_API int set_nvm_context_namespace_details(const NVM_UID namespace_uid,
		const struct namespace_details *p_namespace);

// PCD namespaces
NVM_API int get_nvm_context_pcd_namespace_count();
NVM_API int get_nvm_context_pcd_namespaces(int pcd_nscount,
		struct nvm_namespace_details *p_pcd_nslist);
NVM_API int set_nvm_context_pcd_namespaces(const int pcd_nscount,
	const struct nvm_namespace_details *p_pcd_nslist);

// NFIT
NVM_API int get_nvm_context_nfit_size();
NVM_API int get_nvm_context_nfit(int nfit_size, struct parsed_nfit *p_nfit);
NVM_API int set_nvm_context_nfit(int nfit_size, const struct parsed_nfit *p_nfit);

#ifdef __cplusplus
}
#endif

#endif /* NVM_CONTEXT_H */
