// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const archiveCollection = defineCollection({
    type: 'content',
    schema: ({ image }) =>
        z.object({
            title: z.string(),
            /** 페이지 상단 제목 아래 설명(메타 설명으로도 사용) */
            description: z.string().optional(),
            order: z.number().default(0),
            /** 영문 부제 (예: Defense Robot Competition) */
            subtitle: z.string().optional(),
            /** 제목 아래 칩 (예: 참가 기간, 로봇 이름) */
            chips: z.array(z.string()).optional(),
            /** 강조 칩 (그라데이션) */
            highlight: z.string().optional(),
            /** 페이지 상단 이미지. cutout = 배경 없는 로봇 사진, photo = 일반 사진 */
            cover: image().optional(),
            coverKind: z.enum(['cutout', 'photo']).default('photo'),
            /** 데이터 기반 화면을 쓰는 페이지 */
            template: z.enum(['doc', 'awards', 'events', 'robots', 'roster']).default('doc'),
            /** 구 사이드바 표시 여부 (헤더 메가메뉴 전환 후에는 사용하지 않음) */
            sidebar: z.boolean().optional(),
        }),
});

export const collections = {
    archive: archiveCollection,
};
