import type {CancelablePromise} from "@/client/core/CancelablePromise";
import {OpenAPI} from "@/client/core/OpenAPI";
import {request as __request} from "@/client/core/request";

import type {
    KisilerCreateKisiData,
    KisilerCreateKisiResponse,
    KisilerDeleteKisiData,
    KisilerDeleteKisiResponse,
    KisilerReadKisiData,
    KisilerReadKisilerData,
    KisilerReadKisilerResponse,
    KisilerReadKisiResponse,
    KisilerUpdateKisiData,
    KisilerUpdateKisiResponse,
} from "@/modules/kisiler/types/KisiTypes";

export class KisilerService {
    /**
     * Read Kisiler
     */
    public static readKisiler(
        data: KisilerReadKisilerData = {},
    ): CancelablePromise<KisilerReadKisilerResponse> {
        return __request(OpenAPI, {
            method: "GET",
            url: "/api/v1/kisiler/",
            query: {
                skip: data.skip,
                limit: data.limit,
            },
            errors: {
                422: "Validation Error",
            },
        });
    }

    /**
     * Create Kisi
     */
    public static createKisi(
        data: KisilerCreateKisiData,
    ): CancelablePromise<KisilerCreateKisiResponse> {
        return __request(OpenAPI, {
            method: "POST",
            url: "/api/v1/kisiler/",
            body: data.requestBody,
            mediaType: "application/json",
            errors: {
                422: "Validation Error",
            },
        });
    }

    /**
     * Read Single Kisi
     */
    public static readKisi(
        data: KisilerReadKisiData,
    ): CancelablePromise<KisilerReadKisiResponse> {
        return __request(OpenAPI, {
            method: "GET",
            url: "/api/v1/kisiler/{kimlik_no}",
            path: {
                kimlik_no: data.kimlik_no,
            },
            errors: {
                422: "Validation Error",
            },
        });
    }

    /**
     * Update Kisi
     */
    public static updateKisi(
        data: KisilerUpdateKisiData,
    ): CancelablePromise<KisilerUpdateKisiResponse> {
        return __request(OpenAPI, {
            method: "PATCH",
            url: "/api/v1/kisiler/{kimlik_no}",
            path: {
                kimlik_no: data.kimlik_no,
            },
            body: data.requestBody,
            mediaType: "application/json",
            errors: {
                422: "Validation Error",
            },
        });
    }

    /**
     * Delete Kisi
     */
    public static deleteKisi(
        data: KisilerDeleteKisiData,
    ): CancelablePromise<KisilerDeleteKisiResponse> {
        return __request(OpenAPI, {
            method: "DELETE",
            url: "/api/v1/kisiler/{kimlik_no}",
            path: {
                kimlik_no: data.kimlik_no,
            },
            errors: {
                422: "Validation Error",
            },
        });
    }
}
