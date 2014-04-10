CREATE TABLE statements(
	state_key VARCHAR(8),
	state_text TEXT
);

CREATE TABLE words(
	word_key VARCHAR(8),
	word_text TEXT,
	node_list TEXT
);

CREATE TABLE nodes(
	node_key VARCHAR(8),
	word_list TEXT
);