
import axios from 'axios';
import { ResumeList, ResumeWithDetails } from './data_objects';

const api = axios.create({
	baseURL: 'http://localhost:9093',
});

export const resumeApi = {

	getResumes: async () => {
		const { data } = await api.get('/resume/list');
		return ResumeList.parse(data);
	},

	getResume: async (id: string) => {
		const { data } = await api.get(`/resume/details/${id}`);
		return ResumeWithDetails.parse(data);
	}
};
