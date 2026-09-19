export type UUID = string;
export type ISODateTime = string;

export type WorkspaceRole = 'owner' | 'admin' | 'member' | 'viewer';
export type CardSeverity = string;

export type User = {
	id: UUID;
	email: string;
	full_name: string;
};

export type Workspace = {
	id: UUID;
	name: string;
	color: string;
};

export type WorkspaceMember = {
	workspace_id: UUID;
	user_id: UUID;
	role: WorkspaceRole;
};

export type WorkspaceInfo = {
	id: UUID;
	name: string;
	color: string;
	owner: string;
	role: WorkspaceRole;
};

export type Board = {
	id: UUID;
	name: string;
	bg_img_path: string | null;
	workspace_id: UUID;
};

export type BoardInfo = {
	id: UUID;
	name: string;
	totalCards: number;
};

export type BoardColor = {
	name: string;
	from: string;
	to: string;
};
export type BoardList = {
	id: UUID;
	name: string;
	board_id: UUID;
	position: number;
};

export type ListInfo = {
	id: UUID;
	name: string;
	position: number;
	cards: CardInfo[];
};

export type Card = {
	id: UUID;
	name: string;
	desc: string | null;
	severity: CardSeverity;
	tag: string;
	due_date: ISODateTime;
	list_id: UUID;
};


export type CardInfo = {
	id: UUID;
	name: string;
	severity: CardSeverity;
	tag: string;
	due_date: ISODateTime;
};
export type CardDetails={
	id:UUID;
	desc: string | null;
	checklist: ChecklistInfo[];
}

export type Checklist = {
	id: UUID;
	name: string;
	card_id: UUID;
};

export type ChecklistItem = {
	id: UUID;
	checklist_id: UUID;
	val: string;
	position: number;
	checked: boolean;
	checked_by: UUID | null;
};

export type ChecklistItemInfo = {
	id: UUID;
	val: string;
	position: number;
	checked: boolean;
	checked_by: UUID | null;
};
export type ChecklistInfo = {
	id: UUID;
	name: string;
	items: ChecklistItemInfo[];
};
// Request

export type CreateUserPayload = {
	email: string;
	password: string;
	full_name: string;
};

export type LoginPayload = {
	email: string;
	password: string;
};

export type UpdateUserPayload = {
	email?: string;
	password?: string;
	full_name?: string;
};

// Response
export type RegisterResponse = { success: boolean };
export type LoginResponse = { message: string };
