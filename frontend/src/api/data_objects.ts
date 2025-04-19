import { z } from "zod";

export const Resume = z.object({
	id: z.string().uuid(),
	name: z.string(),
	email: z.string().email(),
	phone: z.string().optional(),
	summary: z.string().optional(),
});

export const ResumeList = Resume.array();

export const Experience = z.object({
	id: z.string().uuid(),
	title: z.string(),
	location: z.string(),
	start_date: z.string().nullable(),
	end_date: z.string().nullable(),
	company: z.string().nullable(),
	description: z.string().nullable()
})

export const Education = z.object({
	id: z.string().uuid(),
	institution: z.string(),
	degree: z.string(),
	field_of_study: z.string().nullable(),
	start_date: z.string().nullable(),
	end_date: z.string().nullable(),
	description: z.string().nullable(),
})

export const Skill = z.object({
	id: z.string().uuid(),
	name: z.string(),
	level: z.string(),
})

export const ResumeWithDetails = z.object({
	id: z.string().uuid(),
	name: z.string(),
	email: z.string().email(),
	phone: z.string().optional(),
	summary: z.string().optional(),
	experiences: z.array(Experience),
	educations: z.array(Education),
	skills: z.array(Skill),
})