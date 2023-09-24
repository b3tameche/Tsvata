
export interface Tag {
    id: number;
    name: string;
    value: string;
}

export interface Job {
    id: number;
    title: string;
    company: string;
    url: string;
    skills: Array<string>;
}

export interface Company {
    company_id: number;
    company_name: string;
    company_website: string;
}