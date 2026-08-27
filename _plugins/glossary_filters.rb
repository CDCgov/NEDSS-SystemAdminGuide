module GlossaryFilters
  def sort_glossary(entries)
    return entries if entries.nil?

    entries.sort_by do |entry|
      term = entry.is_a?(Hash) ? entry["term"] : entry.term
      normalize_term(term)
    end
  end

  private

  def normalize_term(term)
    term.to_s
      .downcase
      .gsub(/[[:punct:]]+/, '')
      .gsub(/\s+/, ' ')
      .strip
  end
end

Liquid::Template.register_filter(GlossaryFilters)
