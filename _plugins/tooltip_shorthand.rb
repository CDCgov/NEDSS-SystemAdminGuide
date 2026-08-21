# Expands the [[key]] / [[key|Visible label]] glossary-tooltip shorthand into the
# term-tooltip.html include, before Liquid and Markdown run.
#
#   [[nlb]]                       -> tooltip with the glossary term's own display text ("NLB")
#   [[classic-nbs|NBS 6]]         -> tooltip whose visible text is the label after the pipe
#
# Rules:
# - `key` must be an existing glossary slug (slugify of a term in _data/glossary.yml).
#   Unknown keys are left untouched and logged as a build warning, so typos stay visible.
# - Shorthand inside fenced (``` / ~~~) or inline (`...`) code is left literal.
# - The include auto-generates a unique id, so the shorthand never carries one.
#
# Authoring guidance lives in contributing/styles.md ("Glossary tooltips").

module TooltipShorthand
  TOKEN  = /\[\[([a-z0-9][a-z0-9-]*)(?:\|([^\]\n]+))?\]\]/
  FENCED = /(?m)^([ \t]*)(`{3,}|~{3,})[^\n]*\n.*?\n\1\2[ \t]*$/
  INLINE = /(`+)(?:(?!\1).)+?\1/
  MARK   = "@@TTSTASH"           # placeholder prefix; @@TTSTASH<idx>@@ can't occur in prose
  RESTORE = /@@TTSTASH(\d+)@@/

  # Cache slug -> canonical display term per site build.
  def self.glossary_slugs(site)
    @cache ||= {}
    @cache[site.object_id] ||= begin
      map = {}
      Array(site.data["glossary"]).each do |entry|
        term = entry.is_a?(Hash) ? entry["term"] : nil
        next if term.to_s.empty?
        map[Jekyll::Utils.slugify(term.to_s)] ||= term.to_s
      end
      map
    end
  end

  # Replace code regions with placeholders so the scanner never touches them.
  def self.mask_code(content)
    stash = []
    masked = content.gsub(FENCED) { |m| stash << m; "#{MARK}#{stash.length - 1}@@" }
    masked = masked.gsub(INLINE)  { |m| stash << m; "#{MARK}#{stash.length - 1}@@" }
    [masked, stash]
  end

  def self.unmask_code(content, stash)
    content.gsub(RESTORE) { stash[Regexp.last_match(1).to_i] }
  end

  def self.expand(content, site, path)
    slugs = glossary_slugs(site)
    content.gsub(TOKEN) do
      key   = Regexp.last_match(1)
      label = Regexp.last_match(2)
      term  = slugs[key]
      if term.nil?
        Jekyll.logger.warn("Tooltip:", "unknown glossary key [[#{key}]] in #{path}")
        Regexp.last_match(0)
      else
        display = label && !label.strip.empty? ? label.strip : term
        %({% include term-tooltip.html key="#{key}" term="#{display.gsub('"', "&quot;")}" %})
      end
    end
  end

  def self.process(doc)
    return unless doc.respond_to?(:content) && doc.content.is_a?(String)
    return unless doc.content.include?("[[")
    return unless %w[.md .markdown].include?(File.extname(doc.path.to_s).downcase)

    masked, stash = mask_code(doc.content)
    doc.content = unmask_code(expand(masked, doc.site, doc.path), stash)
  end
end

Jekyll::Hooks.register([:pages, :documents], :pre_render) { |doc| TooltipShorthand.process(doc) }
